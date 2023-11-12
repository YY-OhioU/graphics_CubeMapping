#version 330 core
out vec4 FragColor;

in vec3 normal;
in vec3 fragPos;

uniform vec3 camPos;
uniform samplerCube environment;

void main()
{
    vec3 I = normalize(fragPos - camPos);
//    vec3 R = refract(I, normalize(normal), 0.4);
    vec3 R = reflect(I, normalize(normal));
    FragColor = vec4(texture(environment, R).rgb, 1.0);
}