# Geometric Foundations Examples

Route: `GEO-01`

This durable examples surface gives the geometric topology bridge a light
foundation before simplex, polyhedron, manifold, and surface work begins. The
examples are original teaching prompts and vocabulary anchors. They are not
copied from any source text.

## Scope

The goal is intuition, not a general affine-geometry theorem prover. These
examples connect existing metric-space and line-plane material to the later
geometric route family.

## Affine Hull

An affine hull is the smallest flat stage that can contain a chosen collection
of points.

Example prompts:

- Two distinct points in the plane determine a line.
- Three non-collinear points in the plane determine the whole plane.
- Three collinear points still determine only a line.

Teaching note:

Ask students to identify which coordinates are free after a point is described
as a weighted average whose weights sum to one.

## Affine Independence

A finite set of points is affinely independent when none of its points is forced
by the affine hull of the others.

Small examples:

- One point is affinely independent.
- Two distinct points are affinely independent.
- Three non-collinear plane points are affinely independent.
- Three collinear plane points are not affinely independent.
- Four points in the plane are always affinely dependent, even if no three are
  collinear.

Bridge forward:

Affine independence is the vocabulary needed for the later `GEO-03` simplex
route. A combinatorial simplex can remember vertices; a geometric simplex also
needs this independence intuition.

## Convex Hull

A convex hull is the smallest convex region containing the chosen points.

Small examples:

- The convex hull of two points is the closed segment between them.
- The convex hull of three non-collinear points is the filled triangle.
- The convex hull of the four corners of a square is the filled square.
- A point inside a triangle does not change the triangle's convex hull.

Diagnostic prompt:

Given four plane points, first decide which ones are extreme. Interior points
are useful for examples, but they are not vertices of the convex hull.

## Barycentric Coordinates

Barycentric coordinates describe a point as a weighted average of vertices. For
a filled triangle, weights are nonnegative and sum to one.

Simple teaching tasks:

- `(1, 0, 0)` names the first vertex.
- `(0, 1, 0)` names the second vertex.
- `(0, 0, 1)` names the third vertex.
- `(1/3, 1/3, 1/3)` names the centroid.
- A zero coordinate places the point on the opposite edge.

Guardrail:

This package should not use barycentric coordinates to make broad claims about
arbitrary geometric realization. The first role is vocabulary and examples.

## Balls, Spheres, And Disks

The existing metric-space material already supports the language of open balls
and closed balls. The geometric bridge uses that language to separate interior,
boundary, and shell intuition.

Examples:

- In the real line, an open ball is an open interval.
- In the Euclidean plane, an open ball is the interior of a round disk.
- A closed disk contains both the interior and its boundary circle.
- A sphere is the shell at fixed distance from a center.
- A disk is the region at distance less than or equal to a radius.

Bridge forward:

Later Euclidean and manifold routes should reuse this distinction: a circle is
a one-dimensional shell, while a disk is a two-dimensional region with boundary.

## Projective-Space Intuition

Projective intuition starts from a simple idea: directions can be treated as
points, and opposite representatives may describe the same direction depending
on the model.

Safe preview examples:

- A line through the origin can be read as one direction.
- Two nonzero vectors on the same origin-line represent the same projective
  point.
- On a circle model, antipodal points can be used as paired representatives of
  the same projective-line point.

Guardrail:

This is only an intuition layer. Full projective classification, algebraic
coordinate charts, and global quotient proofs are deferred to later route work.

## Student Tasks

1. Decide whether three given plane points are collinear before calling them a
   triangle's vertices.
2. Mark which points of a finite plane set are extreme points of its convex
   hull.
3. Interpret barycentric triples with one zero coordinate.
4. Explain why a circle is a boundary shell while a disk is a filled region.
5. Describe, in one sentence, why antipodal representatives can appear in
   projective intuition.

## Route Links

- `GEO-01`: this examples surface.
- `GEO-03`: simplex vocabulary will reuse affine independence and barycentric
  coordinates.
- `GEO-04`: polyhedron intuition will reuse convex hull and filled-region
  language.
- `GEO-06`: Euclidean topology will reuse balls, spheres, disks, and projective
  previews.
