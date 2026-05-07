// Toon pixel shader — banded N·L diffuse with a soft view-direction rim.
// Scalars are packed into uToonCfg = (bands, rim, ambient, _) — they bind through
// the glslMAT "Vectors" page (the "Constants" page injects compile-time defines,
// not runtime uniforms).
in Vertex {
	vec3 worldPos;
	vec3 worldNormal;
} iVert;

uniform vec3 uDiffuse;
uniform vec3 uEmit;
uniform vec3 uLightDir;
uniform vec3 uCamPos;
uniform vec4 uToonCfg;

layout(location = 0) out vec4 fragColor;

void main() {
	vec3 N = normalize(iVert.worldNormal);
	vec3 L = normalize(uLightDir);

	float bands = max(uToonCfg.x, 1.0);
	float rimStrength = uToonCfg.y;
	float ambient = uToonCfg.z;

	float NdotL = max(dot(N, L), 0.0);
	float toon = floor(NdotL * bands) / bands;
	float lit = mix(ambient, 1.0, toon);

	vec3 V = normalize(uCamPos - iVert.worldPos);
	float rim = 1.0 - max(dot(N, V), 0.0);
	rim = smoothstep(0.6, 1.0, rim) * rimStrength;

	vec3 col = uDiffuse * lit + uEmit + vec3(rim);
	fragColor = TDOutputSwizzle(vec4(col, 1.0));
}
