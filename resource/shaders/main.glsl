#version 120

uniform sampler2D sampler;
varying vec2 vec;

void main(void) {
	vec3 color = vec3(texture2D(sampler, vec));
	if (color == vec3(1.0, 0.0, 1.0) {
		discard;
	}
}
