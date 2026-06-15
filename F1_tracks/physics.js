/**
 * RWID Vehicle Physics Engine - Direct Wheel Steering & Precision 6-Degree Rollover Edition
 * Fully synchronized with custom developer UI dashboards.
 */

class RWIDVehiclePhysics {
    constructor() {
        // Factory baseline parameters used when custom toggle is disabled
        this.DEFAULTS = {
            m: 1300.0,       // mass (kg)
            rw: 0.285,       // wheel radius (m)
            B: 1.4375,       // track width (m)
            lf: 1.4373,      // CG to front axle distance (m)
            lr: 1.2247,      // CG to rear axle distance (m)
            Iz: 1808.0,      // yaw moment of inertia (kg*m^2)
            Iw: 1.85,        // wheel inertia (kg*m^2)
            h: 0.3,          // CG height (m)
            P_max: 800000.0, // Upgraded max motor power (W) to support 350 km/h
            s_thresh: 0.15,  // ASR/ABS slip threshold
            Kp: 400.0,       // PID Proportional gain
            Ki: 15.0,        // PID Integral gain
            Kd: 5.0,         // PID Derivative gain
            Cl: 2.5          // Aerodynamic Downforce Coefficient
        };

        this.g = 9.81; // Gravity constant

        // Persistent runtime state vectors
        this.state = {
            vx: 0.1,
            yawRate: 0.0,
            heading: 0.0,
            omegaLeft: 0.0,
            omegaRight: 0.0,
            sLeft: 0.0,
            sRight: 0.0,
            kLeft: 0.0,
            kRight: 0.0,
            T_left: 0.0,
            T_right: 0.0,
            deltaT: 0.0,
            pLoss: 0.0,
            asrActive: false,
            isFlipped: false
        };

        this.speedErrorIntegral = 0.0;
        this.prevSpeedError = 0.0;
    }

    /**
     * Core physics step execution handler.
     * @param {Object} controls - Includes UI inputs, sliders, and parameter dataset
     * @param {number} dt - Step duration delta (seconds)
     */
    update(controls, dt) {
        if (dt <= 0) return this.state;

        // Route parameter source depending on UI configuration switch status
        const p = controls.useCustomSettings ? controls.customParams : this.DEFAULTS;
        const Cl = p.Cl !== undefined ? p.Cl : 2.5;

        // Формула: V(км/год) = V(м/с) * 3.6
        let currentSpeedKMH = this.state.vx * 3.6; // Переводить лінійну швидкість із м/с у км/год для роботи внутрішніх тригерів розгону.

        // =====================================================================
        // ПРАВИЛО ЛОГІКИ АВАРІЇ (Машина перевернута, колеса обертаються в повітрі)
        // =====================================================================
        if (this.state.isFlipped) {
            // Формула: Omega = V_target / r_w
            this.state.omegaLeft = controls.targetSpeed / p.rw; // Занурює оберти лівого колеса в повітрі суворо за повзунком швидкості.
            this.state.omegaRight = controls.targetSpeed / p.rw; // Занурює оберти правого колеса за аналогічним безрезистивним рівнянням.

            this.state.sLeft = 0.0;
            this.state.sRight = 0.0;
            this.state.kLeft = 0.0;
            this.state.kRight = 0.0;
            this.state.yawRate = 0.0;
            this.state.deltaT = 0.0;
            this.state.T_left = 0.0;
            this.state.T_right = 0.0;
            this.state.pLoss = 0.0;

            // Формула: F_drag = 0.5 * Cd * A * p * Vx^2
            let aerodynamicDrag = 0.5 * 0.3 * 2.0 * this.state.vx * this.state.vx; // Вираховує лобовий опір повітря об кузов, що летить шкереберть.

            // Формула: F_roof = m * g * mu_roof
            let roofFrictionForce = p.m * this.g * 0.12; // Обчислює механічну силу тертя голого металу даху об шорсткий гоночний асфальт.

            // Формула: ax = -(F_drag + F_roof) / m
            let ax = -(aerodynamicDrag + roofFrictionForce) / p.m; // Знаходить сповільнення кузова за другим законом Ньютона (тяга моторів = 0).

            // Формула: Vx = Vx + ax * dt
            this.state.vx += ax * dt; // Інтегрує сповільнення по часу, забезпечуючи дуже повільну і реалістичную зупинку машини "на даху".
            if (this.state.vx < 0.1) this.state.vx = 0.1;

            return this.state;
        }

        // 1. РОЗРАХУНОК ВОДІЯ ТА СИСТЕМИ КРУЇЗ-КОНТРОЛЮ (PID & Smart Governor)
        // Формула: e = V_target - Vx
        let speedError = controls.targetSpeed - this.state.vx; // Знаходить лінійну похибку швидкості (наскільки ми відстаємо від цілі).

        // Формула: Integral = Integral + e * dt
        this.speedErrorIntegral += speedError * dt; // Накопичує суму похибок у часі для інтегральної пам'яті PID-алгоритму водія.
        let intLimit = 40.0;

        // Формула: Clamped_Integral = max(-40, min(40, Integral))
        this.speedErrorIntegral = Math.max(-intLimit, Math.min(intLimit, this.speedErrorIntegral)); // Затискає інтеграл (Anti-Windup), прибираючи проскок швидкості.

        // Формула: de/dt = (e_current - e_previous) / dt
        let speedErrorDerivative = (speedError - this.prevSpeedError) / dt; // Вираховує похідну — швидкість зміни похибки між кадрами.
        this.prevSpeedError = speedError;

        // Формула: T_req = Kp * e + Ki * Integral + Kd * (de/dt)
        let T_req = p.Kp * speedError + p.Ki * this.speedErrorIntegral + p.Kd * speedErrorDerivative; // ПІД-рівняння для розрахунку сумарного моменту.

        let T_brake = 0.0;
        let brakingForceBody = 0.0;
        let isBraking = false;

        if (speedError < -2.0) {
            // Формула: T_brake = |T_req| * 2.0
            T_brake = Math.abs(T_req) * 2.0; // Переводить від'ємний момент регулятора в реальний затискний момент колодок на дисках коліс.
            T_brake = Math.min(T_brake, 8000.0);
            T_req = 0.0;
            isBraking = true;

            // Формула: F_brake_body = |e| * m * 0.45
            brakingForceBody = Math.abs(speedError) * p.m * 0.45; // Створює пряму сповільнювальну силу на гальмівні колодки шасі для швидкого "укусу".
            brakingForceBody = Math.min(brakingForceBody, 38000.0);
        }
        else if (speedError <= 0) {
            T_req = 0.0;
            // Формула: Integral = Integral * 0.5
            if (this.speedErrorIntegral > 0) this.speedErrorIntegral *= 0.5; // Скидає накопичений надлишок газу, якщо ми трішки перевищили ліміт.
        }

        if (speedError > 0 && speedError < 4.0) {
            // Формула: factor = e / 4.0
            let approachFactor = speedError / 4.0; // Знаходить відносний коефіцієнт наближення до виставленої користувачем швидкості.

            // Формула: T_req = T_req * factor^1.2
            T_req *= Math.pow(approachFactor, 1.2); // М'яко душить газ (Soft Governor) на підльоті, ліквідуючи перельоти швидкості.
        }

        // ДИНАМІЧНИЙ РОЗГІН З ЛАНЧ-КОНТРОЛЕМ
        if (T_req > 0) {
            if (currentSpeedKMH < 100.0) {
                let steerFactor = Math.max(0.2, 1.0 - Math.abs(controls.steeringAngle) * 2.0); // Знижує буст розгону, якщо колеса викручені.

                // ЛАНЧ-КОНТРОЛЬ: Починаємо з 0.7 і лінійно нарощуємо динаміку до 1.4 суворо паралельно набору 100 км/год
                // Формула: launchFactor = 0.7 + 0.7 * (V_kmh / 100.0)
                let launchFactor = 0.7 + (0.7 * (currentSpeedKMH / 100.0));

                // Формула: T_req = T_req * launchFactor * steerFactor
                T_req *= launchFactor * steerFactor;
            }
            else if (currentSpeedKMH >= 100.0 && currentSpeedKMH <= 250.0) {
                let steerFactor = Math.max(0.2, 1.0 - Math.abs(controls.steeringAngle) * 2.0);

                // Формула: T_req = T_req * 1.4 * steerFactor
                T_req *= 1.4 * steerFactor; // Полка максимального крутного моменту стабільно тримається в діапазоні 100-250 км/год.
            }

            // Плавне спадання крутного моменту після 250 км/год
            if (currentSpeedKMH > 250.0) {
                // Формула: limitFactor = max(0.12, 1.0 - (V_kmh - 250) / 100)
                let motorLimitFactor = Math.max(0.12, 1.0 - (currentSpeedKMH - 250.0) / 100.0); // Поступове падіння тяги інверторів на високих обертах ротора.

                // Формула: T_req = T_req * limitFactor
                T_req *= motorLimitFactor;
            }
        }

        // 2. СТАЦІОНАРНА КІНЕМАТИКА ПОВОРОТУ ТА БІЧНОГО ПРИСКОРЕННЯ (Steady-State Dynamics)
        // Формула: L = lf + lr
        let wheelbase = p.lf + p.lr; // Знаходить загальну геометричну колісну базу автомобіля.

        // ОПТИМІЗАЦІЯ ПРЯМОГО КУТА: Калібруємо вхідний кут коліс, щоб краш на 150 км/год припадав суворо на ~6 градусів
        // Формула: delta_effective = delta_wheels * 0.488
        let effectiveSteerRad = controls.steeringAngle * 0.488; // Коригує кут коліс на асфальті для ідеального збігу з критичною точкою 6°.
        let absSteerRad = Math.max(Math.abs(effectiveSteerRad), 0.0001);

        // Формула: R = L / |delta_effective|
        let turnRadius = wheelbase / absSteerRad; // Розраховує чистий радіус траєкторії кругового руху на основі прямого кута коліс.

        // Формула: ay = Vx^2 / R
        let ay = (this.state.vx * this.state.vx) / turnRadius; // Обчислює стаціонарне відцентрове прискорення. Воно стабільне і не накопичується!

        // Формула: omega_z = (Vx / R) * sign(delta)
        this.state.yawRate = (this.state.vx / turnRadius) * Math.sign(controls.steeringAngle); // Визначає швидкість розвороту кузова боліда.

        // Формула: u_left = Vx - omega_z * (B / 2)
        let u_left = this.state.vx - this.state.yawRate * (p.B / 2.0); // Лінійна швидкість лівої маточини з урахуванням обертання кузова.
        // Формула: u_right = Vx + omega_z * (B / 2)
        let u_right = this.state.vx + this.state.yawRate * (p.B / 2.0); // Лінійна швидкість правої маточини з урахуванням обертання кузова.

        // 3. Slip Ratio tracking processing
        // Формула: s = |u - omega * rw| / max(|u|, |omega * rw|, 0.001)
        this.state.sLeft = Math.abs(u_left - this.state.omegaLeft * p.rw) /
            Math.max(Math.abs(u_left), Math.abs(this.state.omegaLeft * p.rw), 0.001); // Коефіцієнт пробуксовки/блокування лівої шини.
        this.state.sRight = Math.abs(u_right - this.state.omegaRight * p.rw) /
            Math.max(Math.abs(u_right), Math.abs(this.state.omegaRight * p.rw), 0.001); // Коефіцієнт пробуксовки/блокування правої шини.

        // 4. АЕРОДИНАМІЧНА ПРИТИСКНА СИЛА ТА АНАЛІТИЧНИЙ РОЗРАХУНОК ROLLOVER
        // Формула: F_downforce = 0.5 * rho * Cl * A * Vx^2
        let F_downforce = 0.5 * 1.225 * Cl * 2.0 * this.state.vx * this.state.vx; // Обчислює вертикальний тиск повітря на антикрила.

        // Формула: Fz_static_total = ((m * g * lr) / L) + F_downforce
        let Fz_static_total = ((p.m * this.g * p.lr) / (wheelbase)) + F_downforce; // Сумує вагу задньої осі та всю згенеровану притискну силу крил.

        // Формула: Fz_static_wheel = Fz_static_total / 2
        let Fz_static_wheel = Fz_static_total / 2.0; // Поділ загальної вертикальної сили порівну на ліве та праве колесо при їзді прямо.

        // Формула: delta_Fz = (m * ay * h) / B
        let weightTransfer = (p.m * ay * p.h) / p.B; // Розраховує перенесення ваги вбік під дією чистого відцентрового прискорення кузова.

        // Формула: ay_crit = g * B / (2 * h)
        let criticalRolloverThreshold = this.g * (p.B / (2.0 * p.h)); // Математичний поріг перекидання твердого тіла на колесах (~23.5 м/с^2).

        // Формула: bonus = 1.0 + F_downforce / (m * g)
        let downforceBonus = 1.0 + (F_downforce / (p.m * this.g)); // Коефіцієнт збільшення стабільності від притискної сили крил.

        // Порівняння: ay >= ay_crit * bonus
        if (ay >= (criticalRolloverThreshold * downforceBonus) && this.state.vx > 20.0) {
            this.state.isFlipped = true; // Якщо центробіжна сила здолала і колію, і притиск крил — тригериться перевертання.
            return this.state;
        }

        // Формула: Fz_left = max(0, Fz_static_wheel - delta_Fz)
        let Fz_left = Math.max(0.0, Fz_static_wheel - weightTransfer); // Фінальна притискна вага на ліве колесо з урахуванням крену шасі.
        // Формула: Fz_right = max(0, Fz_static_wheel + delta_Fz)
        let Fz_right = Math.max(0.0, Fz_static_wheel + weightTransfer); // Фінальна притискна вага на праве колесо з урахуванням крену шасі.

        // Корекція тертя
        let tireMult = 1.0;
        if (controls.tireType === 'Soft') tireMult = 1.2;
        if (controls.tireType === 'Hard') tireMult = 0.8;

        // Формула: tempFactor = max(0.5, 1.0 - 0.0004 * (T - 40)^2)
        let tempFactor = Math.max(0.5, 1.0 - 0.0004 * Math.pow(controls.trackTemp - 40.0, 2)); // Параболічний зріз зачепу при відхиленні від 40°C.

        // Формула: k = Fz * mu_base * mu_tire * tempFactor
        this.state.kLeft = Fz_left * controls.baseFriction * tireMult * tempFactor; // Кінцева жорсткість зчеплення (стеля Ньютонів) лівого колеса.
        this.state.kRight = Fz_right * controls.baseFriction * tireMult * tempFactor; // Кінцева жорсткість зчеплення (стеля Ньютонів) правого колеса.

        let isTurningLeft = controls.steeringAngle < 0;
        let k_out = isTurningLeft ? this.state.kRight : this.state.kLeft;
        let k_in = isTurningLeft ? this.state.kLeft : this.state.kRight;
        let omega_out = isTurningLeft ? this.state.omegaRight : this.state.omegaLeft;
        let omega_in = isTurningLeft ? this.state.omegaLeft : this.state.omegaRight;

        let T_brake_left = T_brake / 2.0;
        let T_brake_right = T_brake / 2.0;
        let absTriggered = false;

        // 5. АКТИВНА СТАБІЛІЗАЦІЯ, АНТИБУКС (ASR) ТА АНТИБЛОКУВАЛЬНА СИСТЕМА (ABS)
        if (isBraking) {
            if (this.state.sLeft > p.s_thresh && this.state.omegaLeft < u_left / p.rw) {
                // Формула: T_brake_left = T_brake_left * 0.15
                T_brake_left *= 0.15; // Гідроклапан ABS скидає 85% тиску колодок на лівому супорті.
                absTriggered = true;
            }
            if (this.state.sRight > p.s_thresh && this.state.omegaRight < u_right / p.rw) {
                // Формула: T_brake_right = T_brake_right * 0.15
                T_brake_right *= 0.15; // Клапан ABS скидає тиск на правому супорті.
                absTriggered = true;
            }

            this.state.deltaT = 0.0;
            this.state.asrActive = absTriggered;

            // Формула: F_brake_body = F_brake_body * 0.8
            if (absTriggered) brakingForceBody *= 0.8; // Злегка пом'якшує загальний удар гальмування кузова під час модуляції тиску ABS.
        } else {
            if (this.state.sLeft < 0.1 && this.state.sRight < 0.1) {
                this.state.asrActive = false;

                // Формула: num = k_out * omega_in - k_in * omega_out
                let numerator = (k_out * omega_in) - (k_in * omega_out);
                // Формула: den = k_out * omega_in + k_in * omega_out
                let denominator = (k_out * omega_in) + (k_in * omega_out);

                // Формула: deltaT = (num / den) * T_req
                this.state.deltaT = denominator !== 0.0 ? (numerator / denominator) * T_req : 0.0; // Електронний розподіл Torque Vectoring для вкручування в поворот.
            }
            else if (this.state.sLeft > p.s_thresh || this.state.sRight > p.s_thresh) {
                this.state.deltaT = 0.0;

                // Формула: T_req = T_req * 0.35
                T_req *= 0.35; // Протибуксувальна система ASR бачить дикий шліф і моментально зрізає 65% газу моторів.
                this.state.asrActive = true;
            } else {
                let numerator = (k_out * omega_in) - (k_in * omega_out);
                let denominator = (k_out * omega_in) + (k_in * omega_out);
                this.state.deltaT = denominator !== 0.0 ? (numerator / denominator) * T_req : 0.0;
                this.state.asrActive = false;
            }

            if (isTurningLeft) {
                // Формула: T_left = T_req / 2 - deltaT,  T_right = T_req / 2 + deltaT
                this.state.T_left = (T_req / 2.0) - this.state.deltaT;
                this.state.T_right = (T_req / 2.0) + this.state.deltaT;
            } else {
                // Формула: T_left = T_req / 2 + deltaT,  T_right = T_req / 2 - deltaT
                this.state.T_left = (T_req / 2.0) + this.state.deltaT;
                this.state.T_right = (T_req / 2.0) - this.state.deltaT;
            }

            if (Math.abs(this.state.T_left * this.state.omegaLeft) > p.P_max) {
                // Формула: T_left = (P_max / |omega|) * sign(T)
                this.state.T_left = (p.P_max / Math.max(0.1, Math.abs(this.state.omegaLeft))) * Math.sign(this.state.T_left); // Насичення інвертора лівого приводу.
            }
            if (Math.abs(this.state.T_right * this.state.omegaRight) > p.P_max) {
                // Формула: T_right = (P_max / |omega|) * sign(T)
                this.state.T_right = (p.P_max / Math.max(0.1, Math.abs(this.state.omegaRight))) * Math.sign(this.state.T_right); // Насичення інвертора правого приводу.
            }
        }

        // 7. Output dynamic road contact tractive forces
        // Формула: Fx = k * s * sign(omega * rw - u)
        let Fx_left = this.state.kLeft * this.state.sLeft * Math.sign(this.state.omegaLeft * p.rw - u_left); // Поздовжня сила штовхання лівої шини об землю.
        let Fx_right = this.state.kRight * this.state.sRight * Math.sign(this.state.omegaRight * p.rw - u_right); // Поздовжня сила штовхання правої шини об землю.

        // 8. РОЗРАХУНОК КУТОВИХ ШВИДКОСТЕЙ КОЛЕС
        // Формула: omegaDot = (T_motor - Fx * rw - T_brake * sign(omega)) / Iw
        let omegaDot_left = (this.state.T_left - Fx_left * p.rw - T_brake_left * Math.sign(this.state.omegaLeft)) / p.Iw; // Динаміка обертання лівого колісного диска.
        let omegaDot_right = (this.state.T_right - Fx_right * p.rw - T_brake_right * Math.sign(this.state.omegaRight)) / p.Iw; // Динаміка обертання правого колісного диска.

        // Формула: omega = omega + omegaDot * dt
        this.state.omegaLeft += omegaDot_left * dt; // Оновлює кутові оберти лівого колеса на основі балансу моментів.
        this.state.omegaRight += omegaDot_right * dt; // Оновлює кутові оберти правого колеса на основі балансу моментів.

        if (this.state.omegaLeft < 0) this.state.omegaLeft = 0;
        if (this.state.omegaRight < 0) this.state.omegaRight = 0;

        // 9. Process active energy loss tracking
        // Формула: pLoss = Fx * (omega * rw - u)
        let pLossLeft = Fx_left * (this.state.omegaLeft * p.rw - u_left); // Теплові втрати лівої шини від мікроковзання протектора.
        let pLossRight = Fx_right * (this.state.omegaRight * p.rw - u_right); // Теплові втрати правої шини від мікроковзання протектора.

        // Формула: pLoss_total = max(0, pLossLeft + pLossRight)
        this.state.pLoss = Math.max(0.0, pLossLeft + pLossRight); // Сумарне виділення енергії тертя коліс у Ватах для HUD-панелі.

        // 10. РУХ КУЗОВА: ВІДНІМАННЯ ОПОРУ ПОВІТРЯ ТА СИЛИ КОЛОДОК
        // Формула: F_drag = 0.5 * Cd * A * p * Vx^2
        let aerodynamicDrag = 0.5 * 0.3 * 2.0 * this.state.vx * this.state.vx; // Сила лобового опору повітря для умов стабільного ходу.

        // Формула: ax = (Fx_left + Fx_right - F_drag - F_brake_body) / m
        let ax = (Fx_left + Fx_right - aerodynamicDrag - brakingForceBody) / p.m; // Фінальне чисте лінійне прискорення боліда за 2-м законом Ньютона.

        // Формула: Vx = Vx + ax * dt
        this.state.vx += ax * dt; // Оновлює живий показник лінійної швидкості ходу автомобіля вперед.
        if (this.state.vx < 0.1) this.state.vx = 0.1;

        // Оновлення курсу
        // Формула: Heading = Heading + yawRate * dt
        this.state.heading += this.state.yawRate * dt; // Оновлює просторовий компасний курс боліда на основі стаціонарної швидкості рискання.

        return this.state;
    }

    /**
     * Clear active memory cache registers during tracking state resets
     */
    reset() {
        this.speedErrorIntegral = 0.0;
        this.prevSpeedError = 0.0;
        this.state.vx = 0.1;
        this.state.yawRate = 0.0;
        this.state.heading = 0.0;
        this.state.omegaLeft = 0.0;
        this.state.omegaRight = 0.0;
        this.state.pLoss = 0.0;
        this.state.asrActive = false;
        this.state.isFlipped = false;
    }
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = RWIDVehiclePhysics;
}