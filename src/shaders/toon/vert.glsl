// Toon vertex — POP-compatible. Uses TDPos()/TDNormal() so attribute access goes
// through the deform pipeline; required when rendering POPs (copyPOP / pointPOP).
out Vertex {
	vec3 worldPos;
	vec3 worldNormal;
} oVert;

void main() {
	vec3 deformedPos = TDDeform(TDPos()).xyz;
	oVert.worldPos = deformedPos;
	oVert.worldNormal = normalize(TDDeformNorm(TDNormal()));
	gl_Position = TDWorldToProj(vec4(deformedPos, 1.0));
}
