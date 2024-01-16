a = 0;
b = 1;
while (b < 5000) {
    print b;
    b += a;
    a = b - a;
}