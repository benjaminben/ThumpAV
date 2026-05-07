// Billboard vertex — plain textured material. Per-instance orient is set in the POP
// graph by `bb_orient` (glslPOP), so each rectangle is already camera-facing by the
// time it reaches this shader. UV V-flipped to compensate for texture orientation.

out Vertex {
	vec2 uv;
} oVert;

void main() {
	int idx = gl_VertexID % 4;
	vec2 cornerUV;
	if      (idx == 0) cornerUV = vec2(0.0, 0.0); // BL
	else if (idx == 1) cornerUV = vec2(1.0, 0.0); // BR
	else if (idx == 2) cornerUV = vec2(1.0, 1.0); // TR
	else               cornerUV = vec2(0.0, 1.0); // TL

	oVert.uv = vec2(cornerUV.x, 1.0 - cornerUV.y);

	vec3 deformedPos = TDDeform(TDPos()).xyz;
	gl_Position = TDWorldToProj(vec4(deformedPos, 1.0));
}
