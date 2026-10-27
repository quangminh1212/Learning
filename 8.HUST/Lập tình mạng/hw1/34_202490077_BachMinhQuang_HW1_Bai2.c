#include <stdio.h>
#include <math.h>

typedef struct point {
    double x;
    double y;
} point_t;

typedef struct circle {
    point_t center;
    double radius;
} circle_t;

int is_in_circle(point_t *p, circle_t *c) {
    double dx = p->x - c->center.x;
    double dy = p->y - c->center.y;
    double distance_squared = dx * dx + dy * dy;
    double radius_squared = c->radius * c->radius;
    
    if (distance_squared < radius_squared) {
        return 1; // Nằm trong đường tròn
    } else {
        return 0; // Nằm trên hoặc ngoài đường tròn
    }
}

int main() {
    circle_t c;
    point_t p;
    
    printf("Nhap toa do tam (x y) va ban kinh: ");
    scanf("%lf %lf %lf", &c.center.x, &c.center.y, &c.radius);
    
    printf("Nhap toa do diem p (x y): ");
    scanf("%lf %lf", &p.x, &p.y);
    
    if (is_in_circle(&p, &c)) {
        printf("YES\n");
    } else {
        printf("NO\n");
    }
    
    return 0;
}
