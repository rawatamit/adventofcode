#include <stdio.h>

int main()
{
    int a = 0, b = 0, c = 0, d = 0, e = 0, f = 0, g = 0, h = 0, i = 0, j = 0;

    a = 1;

    // set b 65
    b = 65;

    // set c b
    c = b;

    // jnz a 2
    if (a != 0) goto jmp1;

    // jnz 1 5
    goto jmp2;

jmp1:
    // mul b 100
    b *= 100;

    // sub b -100000
    b -= -100000;

    // set c b
    c = b;

    // sub c -17000
    c -= -17000;

jmp2:
    // set f 1
    f = 1;

    // set d 2
    d = 2;

//jmp5b:
    while (d != b)
    {
    // set e 2
    //e = 2;

    if (b % d == 0)
    { f = 0; }

#if 0
//jmp4b:
    do {
    // set g d
    // mul g e
    // sub g b
    g = d * e - b;

    // jnz g 2
    //if (g != 0) { goto jmp3; }
    if (g == 0)
    {
        // set f 0
        f = 0;
    }

    // sub e -1
    e += 1;

    // set g e
    // sub g b
    //g = e - b;

    // jnz g -8
    } while (e != b); //{ goto jmp4b; }
#endif

    // sub d -1
    d += 1;
    }

    // set g d
    // sub g b
    //g = d - b;

    // jnz g -13
    //if (d != b) { goto jmp5b; }

    // jnz f 2
    if (f != 0) { goto jmp6; }

    // sub h -1
    h -= -1;

jmp6:
    // set g b
    g = b;

    // sub g c
    g -= c;

    // jnz g 2
    if (g != 0) { goto jmp7; }

    // jnz 1 3
    goto jmp8;

jmp7:
    // sub b -17
    b -= -17;

    // jnz 1 -23
    goto jmp2;

jmp8:
    printf("%d\n", h);
    return 0;
}
