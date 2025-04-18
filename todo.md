# MVP: given regular triangle with side of 8 * sqrt3, find radius of its circumcircle

- Perpendicular bisectors intersect at point N, which is center of circumcircle
- Height of a regular triangle is a median
- Perpendicular bisector of a regular triangle is a height
- Medians of a triangle intersect in a ratio 2:1, starting from vertex

=> Heights of a regular triangle intersect in center of circumcircle in ratio 2:1, starting from vertex

- Radius is a line segment from polygon edge to circle's center

=> Radius is 2/3 of a regular triangle's height
- If AH is a height of a triangle ABC,
then it's length is sinB * AB, or sinC * AC
- Angles of regular triangle are all 60º

=> Where
R - radius of circumcircle,
a - side of regular triangle
R = a/sqrt(3)

## 1. Implement Polygon
1. build perpendicular bisectors

## 2. Implement Circle
1. build circumcircle around a Polygon

## 3 Define that intersection of perpendicular bisectors is center of circumcircle

## 4. Implement Triangle
1. build heights
2. build medians
3. define that medians intersect in ratio 2:1, starting from vertices

## 5. Implement RegularTriangle
1. Define that medians are heights
2. Define that all angles are 60º
---------
6. Define that radius of circumcircle is a line segment from polygon edge to circumcircle's center
7. Define that radius of circumcircle is 2/3 of regular triangle's height
8. Define that if AH is a height of a triangle ABC, then it's length is sinB * AB, or sinC * A
9. Define that angles of regular triangle are all 60º
10. Derive R = a/sqrt(3)
---------
### 1.1 Build perpendicular bisectors
1. Implement Point, LineSegment, and Angle
2. Create opposing Points on the polygon
If (N edges) % 2 == 1:
    - One opposing Point is a vertex, other is middle of an edge
Else:
    - Both are middles of opposing edges
3. Connect opposing Points to form bisectors as LineSegments and save angle between them as 90º


### 3 Define that intersection of perpendicular bisectors is center of circumcircle
1. Make sure this refers to bisector intersection Point

### 4.1 Build heights of a Triangle
1. Create LineSegments from vertices to opposing edges and save angle between them as 90º

### 4.2 Build medians
1. Create LineSegments from vertices to opposing edges define distance to edge ends as the same

### 4.3 Define that medians intersect in ratio 2:1, starting from vertices
1. Find the intersection
2. Define distance from first vertex to intersection as 2/3*height, and second as 1/3 * height

### 5.1 Define that RegularTriangle's medians are heights
1. Make sure medians refer to heights

### 6. Define that radius of circumcircle is a line segment from polygon vertex to circumcircle's center
1. Build a LineSegment from a vertex Point to center of circumcircle Point

### 7. Define that radius of circumcircle is 2/3 of regular triangle's height
1. Derive the radius' length as 2/3 * height

### 8. Define that if AH is a height of a triangle ABC, then it's length is sinB * AB, or sinC * A
1. Implement RightTriangle
2. Build right triangle from A, B and H
3. Derive H as sinB * A
4. Since B is 60, H is sqrt(3)/2 * A
5. since A is 8 * sqrt(3), H is 8 * sqrt(3) * sqrt(3)/2 = 12

### 10. Find R
1. 2/3 * H = 2/3 * 12 = 8

#### 1.1.2
1. Define where the Point will be placed by arranging all Points on a space relatively.