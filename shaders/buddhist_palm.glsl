// Buddhist Palm imprint — Shadertoy / twigl mainImage
// CPU reference: shaders/buddhist_palm_preview.py (renders the same SDF)
//
// Hand = palm (rounded box) unioned with 5 capsules, via min.
// Cracks = 13 angular spokes, wobbled by sin(r), amplitude growing with r.
// No raymarching: this is a 2D SDF shaded directly, so there is no
// distance-estimate to validate (shader-de does not apply).

float sdCapsule(vec2 p, vec2 a, vec2 b, float r){
    vec2 pa = p - a, ba = b - a;
    float h = clamp(dot(pa,ba)/dot(ba,ba), 0.0, 1.0);
    return length(pa - ba*h) - r;
}

float sdRoundBox(vec2 p, vec2 c, vec2 b, float r){
    vec2 d = abs(p-c) - b;
    return length(max(d,0.0)) + min(max(d.x,d.y),0.0) - r;
}

float hand(vec2 p){
    float d = sdRoundBox(p, vec2(0.0,-0.10), vec2(0.20,0.20), 0.10);   // palm
    d = min(d, sdCapsule(p, vec2(-0.20,0.06), vec2(-0.26,0.44), 0.058)); // index
    d = min(d, sdCapsule(p, vec2(-0.07,0.09), vec2(-0.08,0.55), 0.060)); // middle
    d = min(d, sdCapsule(p, vec2( 0.07,0.09), vec2( 0.10,0.51), 0.058)); // ring
    d = min(d, sdCapsule(p, vec2( 0.19,0.06), vec2( 0.26,0.38), 0.050)); // pinky
    d = min(d, sdCapsule(p, vec2(-0.20,-0.16), vec2(-0.44,0.06), 0.066));// thumb
    return d;
}

float hash1(float n){ return fract(sin(n*127.1)*43758.5453); }

float cracks(vec2 p){
    const int N = 13;
    float r = length(p) + 1e-6;
    float a = atan(p.y, p.x);
    float out_ = 0.0;
    for(int k = 0; k < N; k++){
        float fk  = float(k);
        float jit = (hash1(fk)      - 0.5) * 0.32;
        float amp = 0.55 + hash1(fk+9.0) * 0.45;
        float th  = -3.14159265 + 6.28318530 * fk / float(N) + jit;
        th += 0.22 * sin(r * 7.0 + fk * 2.1);            // wobble
        float da = abs(mod(a - th + 3.14159265, 6.28318530) - 3.14159265);
        float w  = 0.006 + 0.030 * r;
        float line  = clamp(1.0 - da / w, 0.0, 1.0);
        float reach = clamp((r - 0.28) / 0.9, 0.0, 1.0) * exp(-r * 0.8);
        out_ = max(out_, line * reach * amp);
    }
    return out_;
}

void mainImage(out vec4 O, in vec2 F){
    vec2 p = (F - iResolution.xy*0.5) / (iResolution.y*0.42);

    float d = hand(p);
    float c = cracks(p);

    float inside = clamp(-d/0.02, 0.0, 1.0);            // imprint mask
    float rim    = exp(-abs(d)*55.0) * 0.9;             // pressed-up rim
    float depth  = pow(clamp(-d/0.16, 0.0, 1.0), 0.6);  // depression

    vec3 col = vec3(0.42, 0.34, 0.26);                  // earth
    col *= mix(1.0, 0.30 + 0.70*(1.0-depth), step(0.0, inside)*inside);
    col += rim * vec3(0.26, 0.22, 0.16);
    col -= c   * vec3(0.34, 0.30, 0.24);
    col += c*0.20 * vec3(0.05, 0.03, 0.02);

    O = vec4(clamp(col, 0.0, 1.0), 1.0);
}
