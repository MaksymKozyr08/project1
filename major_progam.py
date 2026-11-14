import math
import numpy as np
import trimesh

print("=== Початок генерації деталізованої 3D-моделі акумулятора ===")

# Список для зберігання всіх елементів сцени
all_components = []

# ==============================================================================
# 1. ГЛОБАЛЬНІ ГЕОМЕТРИЧНІ ПАРАМЕТРИ ТА КООРДИНАТИ
# ==============================================================================
# Основні габарити блоку (у відносних одиницях)
BLOCK_HEIGHT = 60.0  # Висота анодної/катодної частини
BLOCK_DEPTH = 30.0  # Глибина (Z-вісь)

# Товщини шарів вздовж осі X (пропорційно до реальних мікроножевих товщин)
THICK_COPPER = 4.0  # Мідний струмознімач (Copper Foil)
THICK_ANODE = 50.0  # Анодний шар (Anode)
THICK_SEPARATOR = 10.0  # Сепараційна мембрана (Separator)
THICK_CATHODE = 50.0  # Катодний шар (Cathode)
THICK_ALUMINUM = 4.0  # Алюмінієвий струмознімач (Aluminum Foil)

# Розрахунок стартових точок вздовж осі X для кожного шару
x_copper_center = THICK_COPPER / 2.0
x_anode_start = THICK_COPPER
x_anode_center = x_anode_start + (THICK_ANODE / 2.0)

x_sep_start = x_anode_start + THICK_ANODE
x_sep_center = x_sep_start + (THICK_SEPARATOR / 2.0)

x_cathode_start = x_sep_start + THICK_SEPARATOR
x_cathode_center = x_cathode_start + (THICK_CATHODE / 2.0)

x_alum_start = x_cathode_start + THICK_CATHODE
x_alum_center = x_alum_start + (THICK_ALUMINUM / 2.0)

TOTAL_WIDTH = x_alum_start + THICK_ALUMINUM

# Фіксація випадковості для повторюваності форми гранул
np.random.seed(101)


# ==============================================================================
# 2. МІДНИЙ СТРУМОЗНІМАЧ (COPPER FOIL - ЛІВА ПЛАСТИНА)
# ==============================================================================
print("--> Генерація мідного колектора (Copper Foil)...")

# Основна пластина фольги
copper_plate = trimesh.creation.box(
    extents=[THICK_COPPER, BLOCK_HEIGHT, BLOCK_DEPTH]
)
copper_plate.apply_translation(
    [x_copper_center, BLOCK_HEIGHT / 2.0, BLOCK_DEPTH / 2.0]
)
copper_plate.visual.face_colors = [184, 115, 51, 255]  # Характерний мідний колір
all_components.append(copper_plate)

# Додаємо виступаючий верхній контактний Язичок (Tab) над мідною фольгою
copper_tab = trimesh.creation.box(extents=[THICK_COPPER * 0.8, 8.0, 6.0])
copper_tab.apply_translation(
    [x_copper_center, BLOCK_HEIGHT + 4.0, BLOCK_DEPTH / 2.0]
)
copper_tab.visual.face_colors = [195, 125, 60, 255]
all_components.append(copper_tab)


# ==============================================================================
# 3. АНОДНИЙ ШАР (ANODE - ВУГЛЕЦЕВА МАТРИЦЯ ТА ГРАФІТОВІ ГРАНУЛИ)
# ==============================================================================
print("--> Генерація анодного блоку (Графіт + Вуглецева основа)...")

# Пориста пористість/матриця (темна основа анода)
anode_matrix = trimesh.creation.box(
    extents=[THICK_ANODE, BLOCK_HEIGHT, BLOCK_DEPTH]
)
anode_matrix.apply_translation(
    [x_anode_center, BLOCK_HEIGHT / 2.0, BLOCK_DEPTH / 2.0]
)
anode_matrix.visual.face_colors = [35, 38, 42, 255]  # Темно-сірий/вугільний
all_components.append(anode_matrix)

# Масив неправильних графітових частинок (Anode Graphite Particles)
NUM_ANODE_PARTICLES = 220
print(f"    Формування {NUM_ANODE_PARTICLES} нерівних гранул анода...")

for i in range(NUM_ANODE_PARTICLES):
    # Радіус гранули
    r = np.random.uniform(2.8, 5.2)

    # Генерація координат із зосередженням біля переднього зрізу
    px = np.random.uniform(x_anode_start + r, x_anode_start + THICK_ANODE - r)
    py = np.random.uniform(r, BLOCK_HEIGHT - r)
    # Зсув на передній план (Z = BLOCK_DEPTH) для максимальної деталізації
    pz = np.random.uniform(BLOCK_DEPTH * 0.35, BLOCK_DEPTH + 1.2)

    # Створення деформованої сфери (імітація колотого графіту)
    particle = trimesh.creation.icosphere(subdivisions=2, radius=r)

    # Негабаритне масштабування вздовж трьох осей для надання унікальної форми
    scale_factors = np.random.uniform(0.65, 1.35, size=3)
    particle.apply_scale(scale_factors)

    # Випадкове обертання гранули у просторі
    rot_matrix = trimesh.transformations.random_rotation_matrix()
    particle.apply_transform(rot_matrix)

    # Переміщення в розраховану позицію
    particle.apply_translation([px, py, pz])

    # Градієнтне забарвлення гранул (від світло-сірого до темно-металевого)
    shade = np.random.randint(110, 160)
    particle.visual.face_colors = [shade, shade + 5, shade + 10, 255]

    all_components.append(particle)


# ==============================================================================
# 4. СЕПАРАТОР (SEPARATOR - ПОРИСТА МЕМБРАНА)
# ==============================================================================
print("--> Генерація пористого сепаратора (Separator Membrane)...")

# Основа сепаратора
sep_base = trimesh.creation.box(
    extents=[THICK_SEPARATOR, BLOCK_HEIGHT, BLOCK_DEPTH]
)
sep_base.apply_translation(
    [x_sep_center, BLOCK_HEIGHT / 2.0, BLOCK_DEPTH / 2.0]
)
sep_base.visual.face_colors = [225, 230, 235, 255]  # Біло-кремовий
all_components.append(sep_base)

# Деталізація пористої структури сепаратора (поздовжні волокна/пори)
NUM_SEP_PORES = 180
print(f"    Додавання {NUM_SEP_PORES} мікроволокон сепаратора...")

for _ in range(NUM_SEP_PORES):
    pore_r = np.random.uniform(0.4, 0.9)
    pore_h = np.random.uniform(2.0, 5.0)

    px = np.random.uniform(
        x_sep_start + pore_r, x_sep_start + THICK_SEPARATOR - pore_r
    )
    py = np.random.uniform(1.0, BLOCK_HEIGHT - 1.0)
    pz = np.random.uniform(BLOCK_DEPTH * 0.5, BLOCK_DEPTH + 0.8)

    fiber = trimesh.creation.cylinder(radius=pore_r, height=pore_h)

    # Обертаємо волокна в площині зрізу
    fiber_rot = trimesh.transformations.rotation_matrix(
        np.random.uniform(0, math.pi), [1, 0, 0]
    )
    fiber.apply_transform(fiber_rot)
    fiber.apply_translation([px, py, pz])

    # Світло-сірі волокна
    fiber.visual.face_colors = [190, 195, 200, 255]
    all_components.append(fiber)


# ==============================================================================
# 5. КАТОДНИЙ ШАР (CATHODE - ОКСИДНА МАТРИЦЯ ТА СФЕРИЧНІ КУЛЬКИ)
# ==============================================================================
print("--> Генерація катодного блоку (Оксидна маса + Активні кульки)...")

# Катодна матриця (чорне сполучне)
cathode_matrix = trimesh.creation.box(
    extents=[THICK_CATHODE, BLOCK_HEIGHT, BLOCK_DEPTH]
)
cathode_matrix.apply_translation(
    [x_cathode_center, BLOCK_HEIGHT / 2.0, BLOCK_DEPTH / 2.0]
)
cathode_matrix.visual.face_colors = [18, 20, 22, 255]  # Глибокий чорний
all_components.append(cathode_matrix)

# Масив сферичних катодних кульок (Lithium Metal Oxide Spheres)
NUM_CATHODE_SPHERES = 550
print(f"    Генерація {NUM_CATHODE_SPHERES} сферичних елементів катода...")

for i in range(NUM_CATHODE_SPHERES):
    r = np.random.uniform(1.2, 2.6)

    px = np.random.uniform(
        x_cathode_start + r, x_cathode_start + THICK_CATHODE - r
    )
    py = np.random.uniform(r, BLOCK_HEIGHT - r)
    pz = np.random.uniform(BLOCK_DEPTH * 0.35, BLOCK_DEPTH + 1.0)

    # Сфери високої деталізації
    sphere = trimesh.creation.icosphere(subdivisions=2, radius=r)
    sphere.apply_translation([px, py, pz])

    # Яскраво-білий/сріблястий колір для контрасту з анодом
    brightness = np.random.randint(230, 255)
    sphere.visual.face_colors = [brightness, brightness, brightness, 255]

    all_components.append(sphere)


# ==============================================================================
# 6. АЛЮМІНІЄВИЙ СТРУМОЗНІМАЧ (ALUMINUM FOIL - ПРАВА ПЛАСТИНА)
# ==============================================================================
print("--> Генерація алюмінієвого колектора (Aluminum Foil)...")

# Алюмінієва фольга
alum_plate = trimesh.creation.box(
    extents=[THICK_ALUMINUM, BLOCK_HEIGHT, BLOCK_DEPTH]
)
alum_plate.apply_translation(
    [x_alum_center, BLOCK_HEIGHT / 2.0, BLOCK_DEPTH / 2.0]
)
alum_plate.visual.face_colors = [200, 205, 210, 255]  # Сріблястий алюміній
all_components.append(alum_plate)

# Верхній контактний язичок для алюмінію
alum_tab = trimesh.creation.box(extents=[THICK_ALUMINUM * 0.8, 8.0, 6.0])
alum_tab.apply_translation(
    [x_alum_center, BLOCK_HEIGHT + 4.0, BLOCK_DEPTH / 2.0]
)
alum_tab.visual.face_colors = [215, 220, 225, 255]
all_components.append(alum_tab)


# ==============================================================================
# 7. ЗВЕДЕНА ВЕРХНЯ ШИНА ТА КОННЕКТОРИ (TOP WIRE CONNECTORS & BRIDGE)
# ==============================================================================
print("--> Створення зовнішньої струмопровідної системи (Дроти та мости)...")

wire_radius = 1.4
wire_color = [110, 115, 120, 255]  # Металевий темно-сірий

# 1. Ліва вертикальна стійка над міддю
left_post = trimesh.creation.cylinder(radius=wire_radius, height=18.0)
left_post.apply_translation(
    [x_copper_center, BLOCK_HEIGHT + 13.0, BLOCK_DEPTH / 2.0]
)
left_post.visual.face_colors = wire_color
all_components.append(left_post)

# 2. Права вертикальна стійка над алюмінієм
right_post = trimesh.creation.cylinder(radius=wire_radius, height=18.0)
right_post.apply_translation(
    [x_alum_center, BLOCK_HEIGHT + 13.0, BLOCK_DEPTH / 2.0]
)
right_post.visual.face_colors = wire_color
all_components.append(right_post)

# 3. Горизонтальний з'єднувальний міст (Bridge)
bridge_length = TOTAL_WIDTH
horizontal_bridge = trimesh.creation.cylinder(
    radius=wire_radius, height=bridge_length
)

# Поворот циліндра уздовж осі X
rot_x = trimesh.transformations.rotation_matrix(math.pi / 2.0, [0, 1, 0])
horizontal_bridge.apply_transform(rot_x)
horizontal_bridge.apply_translation(
    [TOTAL_WIDTH / 2.0, BLOCK_HEIGHT + 22.0, BLOCK_DEPTH / 2.0]
)
horizontal_bridge.visual.face_colors = wire_color
all_components.append(horizontal_bridge)

# 4. Центральний вихідний контактний термінал (Main Terminal Pin)
main_terminal = trimesh.creation.cylinder(radius=1.8, height=12.0)
main_terminal.apply_translation(
    [TOTAL_WIDTH / 2.0, BLOCK_HEIGHT + 28.0, BLOCK_DEPTH / 2.0]
)
main_terminal.visual.face_colors = [140, 145, 150, 255]
all_components.append(main_terminal)

# Шапочка на центральному терміналі
terminal_cap = trimesh.creation.icosphere(subdivisions=2, radius=2.5)
terminal_cap.apply_translation(
    [TOTAL_WIDTH / 2.0, BLOCK_HEIGHT + 34.0, BLOCK_DEPTH / 2.0]
)
terminal_cap.visual.face_colors = [160, 165, 170, 255]
all_components.append(terminal_cap)


# ==============================================================================
# 8. ЗБИРАННЯ СЦЕНИ ТА ЕКСПОРТ
# ==============================================================================
print("--> Збирання підсумкової 3D-сцени...")
scene = trimesh.Scene(all_components)

output_filename = "detailed_battery.glb"
print(f"--> Експорт у файл: {output_filename}...")
scene.export(output_filename)

print("=== УСПІШНО ЗАВЕРШЕНО! ===")
print(f"Файл '{output_filename}' збережено у поточній директорії.")
print("Запустіть перегляд за допомогою scene.show()")

# Запуск візуалізації
scene.show()