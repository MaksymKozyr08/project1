typedef struct {
    union {
        unsigned long long num;
        struct {
            unsigned long long mantissa : 29;
            unsigned long long characteristics : 12;
            unsigned long long sign : 1;
        } bits;
    };
} IEEE_format ;

IEEE_format toIEEE (double n) {
    IEEE_format res;
    res.num = 0;

    if (n == 0.0) return res;
    if (n<0) {
        res.bits.sign = 1;
        n=-n;
    } else {
        res.bits.sign = 0;
    }
    if (n==INFINITY || n==-INFINITY) {
        res.bits.characteristics = (unsigned long long)(4095);
        res.bits.mantissa = (unsigned long long)(0);
        return res;
    }
    if (std::isnan(n)) {
        res.bits.characteristics = (unsigned long long)(4095);
        res.bits.mantissa = (unsigned long long)(1);
        return res;
    }

    int charact=0;
    if (n<1) {
        while (n<1) {
            n*=2;
            charact--;
        }
    } else {
        while (n>=2) {
            n/=2;
            charact++;
        }
    }

    res.bits.characteristics = (unsigned long long)(charact + 2047);
    res.bits.mantissa = (unsigned long long)((n-1) * pow(2, 29) + 0.5); //0.5 для правильного округлення

    return res;
}

double fromIEEE (IEEE_format n) {

    if (n.bits.characteristics == 4095 && n.bits.mantissa != 0) return NAN;
    if (n.bits.characteristics == 4095 && n.bits.mantissa == 0) return (n.bits.sign) ? -INFINITY : INFINITY;
    if (n.bits.characteristics == 0 && n.bits.mantissa == 0) return 0.0;

    double mantissa = 1.0 + ((double)n.bits.mantissa / pow(2, 29));
    int charact = (int)n.bits.characteristics - 2047;
    double res = mantissa * pow(2, charact);

    return (n.bits.sign) ? -res : res;
}