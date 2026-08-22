// Billboard pixel â€” texture with alpha cutout. Hard-discard transparent pixels so the
// texture's transparent regions (e.g. GIF/sprite alpha) don't draw.
// uTex3d.x > 0.5 switches sampling to the rolling 3D texture cache (tex3d TOP):
// each particle reads slice fract(bbW + phase) â€” bbW is its stable per-particle
// offset, uTex3d.y the shared playback phase (held at 0 while frozen, so every
// billboard keeps its own single frame).

in Vertex {
	vec2 uv;
	flat float bbW;
} iVert;

uniform sampler2D sTex;
uniform sampler3D sTex3d;
uniform vec4 uTex3d; // x = tex3d enable, y = playback phase

layout(location = 0) out vec4 fragColor;

void main() {
	vec4 c;
	if (uTex3d.x > 0.5) {
		c = texture(sTex3d, vec3(iVert.uv, fract(iVert.bbW + uTex3d.y)));
	} else {
		c = texture(sTex, iVert.uv);
	}
	if (c.a < 0.05) discard;
	fragColor = TDOutputSwizzle(vec4(c.rgb, 1.0));
}
