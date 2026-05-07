// Billboard pixel — texture with alpha cutout. Hard-discard transparent pixels so the
// texture's transparent regions (e.g. GIF/sprite alpha) don't draw.

in Vertex {
	vec2 uv;
} iVert;

uniform sampler2D sTex;

layout(location = 0) out vec4 fragColor;

void main() {
	vec4 c = texture(sTex, iVert.uv);
	if (c.a < 0.05) discard;
	fragColor = TDOutputSwizzle(vec4(c.rgb, 1.0));
}
