// Billboard vertex â€” plain textured material. Per-instance orient is set in the POP
// graph by `bb_orient` (glslPOP), so each rectangle is already camera-facing by the
// time it reaches this shader. UV V-flipped to compensate for texture orientation.
// bbW (per-particle tex3d slice offset, computed in bb_orient and copied onto the
// instanced quads by the copyPOP template-attribute transfer) rides through to the
// pixel shader for sampler3D slice lookups.

out Vertex {
	vec2 uv;
	flat float bbW;
} oVert;

void main() {
	int idx = gl_VertexID % 4;
	vec2 cornerUV;
	if      (idx == 0) cornerUV = vec2(0.0, 0.0); // BL
	else if (idx == 1) cornerUV = vec2(1.0, 0.0); // BR
	else if (idx == 2) cornerUV = vec2(1.0, 1.0); // TR
	else               cornerUV = vec2(0.0, 1.0); // TL

	// U-flipped too: the POP-oriented quad's BL->BR edge points screen-LEFT
	// from the camera's view, so raw U renders textures horizontally mirrored.
	oVert.uv = vec2(1.0 - cornerUV.x, 1.0 - cornerUV.y);
	oVert.bbW = TDAttrib_bbW();

	vec3 deformedPos = TDDeform(TDPos()).xyz;
	gl_Position = TDWorldToProj(vec4(deformedPos, 1.0));
}
