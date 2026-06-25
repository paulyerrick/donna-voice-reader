import React from "react";

export default function LumenVoiceReader() {
  const html = `<section class="bg-[#070709] text-slate-200 font-['Inter'] antialiased overflow-x-hidden min-h-screen selection:bg-fuchsia-500/30 selection:text-white">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&amp;display=swap" rel="stylesheet">

<div id="fluid-container" class="fixed inset-0 z-0 opacity-90 pointer-events-none mix-blend-screen"></div>

<div class="fixed inset-0 z-0 pointer-events-none" style="background: radial-gradient(circle at center, transparent 0%, #070709 75%);"></div>

<nav class="fixed top-0 w-full z-50 border-b border-white/[0.05] bg-[#070709]/50 backdrop-blur-xl">
        <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between text-sm">
            <div class="flex items-center gap-2 font-medium text-white">
                <div class="w-7 h-7 rounded-lg flex items-center justify-center" style="background: linear-gradient(135deg, #ff00aa, #00e5ff);">
                    <iconify-icon icon="solar:soundwave-linear" width="16" class="text-white"></iconify-icon>
                </div>
                <span class="tracking-tight">Lumen</span>
            </div>
            <div class="hidden md:flex items-center gap-8 text-slate-400 font-medium text-sm">
                <a href="#" class="hover:text-white transition-colors">Library</a>
                <a href="#" class="hover:text-white transition-colors">Voices</a>
                <a href="#" class="hover:text-white transition-colors">History</a>
            </div>
            <div class="flex items-center gap-4">
                <button class="text-slate-400 hover:text-white transition-colors hidden md:flex items-center gap-1.5">
                    <iconify-icon icon="solar:settings-linear" width="18"></iconify-icon>
                </button>
                <div style="background: linear-gradient(to right bottom, rgba(255,0,170,0.5), rgba(0,229,255,0.5)); padding: 1px;" class="rounded-full">
                    <button class="bg-[#070709] hover:bg-white/[0.04] transition-colors text-white px-4 py-1.5 rounded-full font-medium text-sm flex items-center gap-1.5">
                        <iconify-icon icon="solar:crown-minimalistic-linear" width="15"></iconify-icon>
                        Upgrade
                    </button>
                </div>
            </div>
        </div>
    </nav>

<main class="relative z-10 min-h-screen flex flex-col items-center justify-center px-5 pt-28 pb-16 gap-8">

        <div class="text-center flex flex-col items-center gap-3 max-w-xl">
            <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full border border-white/10 text-xs font-medium text-slate-300" style="background: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0) 100%); backdrop-filter: blur(8px);">
                <span id="status-dot" class="w-1.5 h-1.5 rounded-full bg-slate-500 transition-colors"></span>
                <span id="status-label">Ready to read</span>
            </div>
            <h1 class="text-3xl md:text-4xl font-semibold tracking-tight text-white leading-tight">
                Paste it. Press play.<br>
                <span class="text-transparent bg-clip-text" style="background-image: linear-gradient(90deg, #ff00aa, #ffaa00, #00e5ff); -webkit-background-clip: text;">Let it speak.</span>
            </h1>
        </div>

        <!-- Glass text bubble with gradient border -->
        <div class="w-full max-w-2xl" style="background: linear-gradient(140deg, rgba(255,0,170,0.35), rgba(0,229,255,0.25), rgba(255,255,255,0.05)); padding: 1px; border-radius: 1.5rem;">
            <div class="rounded-[calc(1.5rem-1px)] p-1.5" style="background: rgba(12,12,16,0.55); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);">

                <!-- Editable text area -->
                <div class="relative rounded-2xl overflow-hidden">
                    <textarea id="reader-input" rows="6" placeholder="Paste or type the text you'd like read aloud…" class="w-full max-h-72 min-h-[140px] resize-none bg-transparent text-slate-100 placeholder:text-slate-500 text-base leading-relaxed px-5 py-4 outline-none overflow-y-auto" style="white-space: pre-wrap; word-wrap: break-word;"></textarea>
                </div>

                <!-- Toolbar -->
                <div class="flex items-center justify-between flex-wrap gap-3 px-3 pb-2 pt-2 border-t border-white/[0.06]">
                    <div class="flex items-center gap-2 text-slate-400 text-xs">
                        <span id="word-count">0 words</span>
                        <span class="text-slate-600">·</span>
                        <span id="read-time">~0 min</span>
                    </div>
                    <div class="flex items-center gap-2">
                        <!-- Voice selector (custom dropdown) -->
                        <div class="relative" id="voice-dd">
                            <button id="voice-btn" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/[0.08] bg-white/[0.03] hover:bg-white/[0.06] text-slate-200 text-xs font-medium transition-colors">
                                <iconify-icon icon="solar:user-speak-rounded-linear" width="15"></iconify-icon>
                                <span id="voice-label">Aria</span>
                                <iconify-icon icon="solar:alt-arrow-down-linear" width="14" class="text-slate-500"></iconify-icon>
                            </button>
                            <div id="voice-menu" class="hidden absolute bottom-full right-0 mb-2 w-40 rounded-xl border border-white/[0.08] p-1 z-30" style="background: rgba(16,16,22,0.92); backdrop-filter: blur(20px);">
                                <button class="voice-opt w-full text-left px-3 py-2 rounded-lg text-xs text-slate-200 hover:bg-white/[0.06] transition-colors">Aria</button>
                                <button class="voice-opt w-full text-left px-3 py-2 rounded-lg text-xs text-slate-200 hover:bg-white/[0.06] transition-colors">Orion</button>
                                <button class="voice-opt w-full text-left px-3 py-2 rounded-lg text-xs text-slate-200 hover:bg-white/[0.06] transition-colors">Nova</button>
                                <button class="voice-opt w-full text-left px-3 py-2 rounded-lg text-xs text-slate-200 hover:bg-white/[0.06] transition-colors">Sage</button>
                            </div>
                        </div>
                        <button id="clear-btn" class="px-3 py-1.5 rounded-lg border border-white/[0.08] bg-white/[0.03] hover:bg-white/[0.06] text-slate-300 text-xs font-medium transition-colors flex items-center gap-1.5">
                            <iconify-icon icon="solar:eraser-linear" width="14"></iconify-icon>
                            Clear
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Playback controls -->
        <div class="w-full max-w-2xl flex flex-col gap-4">
            <!-- Progress -->
            <div class="flex items-center gap-3 text-xs text-slate-400 font-medium">
                <span id="time-current">0:00</span>
                <div id="progress-track" class="flex-1 h-1.5 rounded-full bg-white/[0.08] relative cursor-pointer overflow-hidden">
                    <div id="progress-fill" class="absolute left-0 top-0 h-full rounded-full" style="width:0%; background: linear-gradient(90deg, #ff00aa, #00e5ff);"></div>
                </div>
                <span id="time-total">0:00</span>
            </div>

            <!-- Transport -->
            <div class="flex items-center justify-center gap-4">
                <button class="w-10 h-10 rounded-full border border-white/[0.08] bg-white/[0.03] hover:bg-white/[0.06] transition-colors flex items-center justify-center text-slate-300">
                    <iconify-icon icon="solar:rewind-back-linear" width="18"></iconify-icon>
                </button>
                <div style="background: linear-gradient(135deg, #ff00aa, #00e5ff); padding: 2px; border-radius: 9999px;" class="shadow-[0_0_40px_-8px_rgba(255,0,170,0.4)]">
                    <button id="play-btn" class="w-14 h-14 rounded-full bg-[#0c0c10] hover:bg-[#14141a] transition-colors flex items-center justify-center text-white">
                        <iconify-icon id="play-icon" icon="solar:play-bold" width="24"></iconify-icon>
                    </button>
                </div>
                <button class="w-10 h-10 rounded-full border border-white/[0.08] bg-white/[0.03] hover:bg-white/[0.06] transition-colors flex items-center justify-center text-slate-300">
                    <iconify-icon icon="solar:rewind-forward-linear" width="18"></iconify-icon>
                </button>
            </div>

            <!-- Speed (custom slider) -->
            <div class="flex items-center gap-4 max-w-md w-full mx-auto mt-2">
                <iconify-icon icon="solar:hare-linear" width="18" class="text-slate-500"></iconify-icon>
                <div id="speed-track" class="flex-1 h-1.5 rounded-full bg-white/[0.08] relative cursor-pointer">
                    <div id="speed-fill" class="absolute left-0 top-0 h-full rounded-full" style="width:40%; background: linear-gradient(90deg, #ffaa00, #00e5ff);"></div>
                    <div id="speed-thumb" class="absolute top-1/2 w-3.5 h-3.5 rounded-full bg-white shadow -translate-y-1/2" style="left:40%; transform: translate(-50%,-50%);"></div>
                </div>
                <span id="speed-label" class="text-xs text-slate-400 font-medium w-9 text-right">1.0x</span>
            </div>
        </div>
    </main>

<section class="relative z-10 max-w-5xl mx-auto px-6 pb-28">
        <h2 id="reveal-text" class="text-2xl md:text-3xl font-medium tracking-tight text-white leading-snug text-center max-w-3xl mx-auto">
            A reading companion that listens with you, turning any block of text into natural, expressive narration in seconds.
        </h2>
        <div class="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="p-6 rounded-2xl border border-white/[0.06] bg-white/[0.02]" style="backdrop-filter: blur(6px);">
                <div class="w-10 h-10 rounded-full flex items-center justify-center border border-white/10 mb-4" style="background: linear-gradient(135deg, rgba(255,0,170,0.12), transparent);">
                    <iconify-icon icon="solar:microphone-3-linear" width="20" class="text-fuchsia-400"></iconify-icon>
                </div>
                <h3 class="text-base font-medium text-white mb-2 tracking-tight">Lifelike Voices</h3>
                <p class="text-sm text-slate-400 leading-relaxed">Four expressive narrators with natural pacing, breath, and intonation.</p>
            </div>
            <div class="p-6 rounded-2xl border border-white/[0.06] bg-white/[0.02]" style="backdrop-filter: blur(6px);">
                <div class="w-10 h-10 rounded-full flex items-center justify-center border border-white/10 mb-4" style="background: linear-gradient(135deg, rgba(255,170,0,0.12), transparent);">
                    <iconify-icon icon="solar:slider-horizontal-linear" width="20" class="text-amber-400"></iconify-icon>
                </div>
                <h3 class="text-base font-medium text-white mb-2 tracking-tight">Tune the Tempo</h3>
                <p class="text-sm text-slate-400 leading-relaxed">Glide from a gentle read to a brisk skim with precise speed control.</p>
            </div>
            <div class="p-6 rounded-2xl border border-white/[0.06] bg-white/[0.02]" style="backdrop-filter: blur(6px);">
                <div class="w-10 h-10 rounded-full flex items-center justify-center border border-white/10 mb-4" style="background: linear-gradient(135deg, rgba(0,229,255,0.12), transparent);">
                    <iconify-icon icon="solar:download-minimalistic-linear" width="20" class="text-cyan-400"></iconify-icon>
                </div>
                <h3 class="text-base font-medium text-white mb-2 tracking-tight">Save &amp; Listen</h3>
                <p class="text-sm text-slate-400 leading-relaxed">Export any reading as audio and pick up right where you left off.</p>
            </div>
        </div>
    </section>

<script src="https://cdn.tailwindcss.com"></script>
<script src="https://code.iconify.design/iconify-icon/1.0.7/iconify-icon.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js"></script>
<script type="module">
        import { Renderer, Program, Mesh, Color, Triangle } from 'https://cdn.jsdelivr.net/npm/ogl@1.0.0/+esm';

        const MAX_STRANDS = 12, MAX_COLORS = 8;
        const VERT = \`#version 300 es
        in vec2 position;
        void main(){ gl_Position = vec4(position,0.0,1.0); }\`;
        const FRAG = \`#version 300 es
        precision highp float;
        uniform float uTime; uniform vec2 uResolution;
        uniform vec3 uColors[\${MAX_COLORS}]; uniform int uColorCount; uniform int uStrandCount;
        uniform float uSpeed,uAmplitude,uWaviness,uThickness,uGlow,uTaper,uSpread,uHueShift,uIntensity,uOpacity,uScale,uSaturation;
        out vec4 fragColor; const float PI=3.14159265;
        vec3 samplePalette(float t){ t=fract(t); float s=t*float(uColorCount); int idx=int(floor(s)); float b=fract(s); int n=idx+1; if(n>=uColorCount)n=0; return mix(uColors[idx],uColors[n],b); }
        void main(){
          vec2 uv=(gl_FragCoord.xy-0.5*uResolution)/uResolution.y; uv/=max(uScale,0.0001);
          float e=0.06+uIntensity*0.94;
          float env=pow(max(cos(uv.x*PI*1.1),0.0),uTaper);
          vec3 col=vec3(0.0);
          for(int i=0;i<\${MAX_STRANDS};i++){
            if(i>=uStrandCount)break;
            float fi=float(i); float ph=fi*1.7*uSpread; float freq=(1.5+fi*0.2)*uWaviness; float spd=1.0+fi*0.8;
            float tt=uTime*uSpeed;
            float w=sin(uv.x*freq+tt*spd+ph)*0.70+sin(uv.x*freq*1.2-tt*spd*0.6+ph*1.5)*0.30;
            float amp=(0.1+0.05*e)*env*uAmplitude; float y=w*amp;
            float d=abs(uv.y-y); float thick=(0.001+0.04*e)*(0.4+env)*uThickness;
            float g=thick/(d+thick*0.5); g=g*g;
            float h=fi/float(uStrandCount)+uv.x*0.2+uTime*0.05+uHueShift;
            col+=samplePalette(h)*g*env;
          }
          col*=0.5+0.6*e; col=1.0-exp(-col*uGlow);
          float gray=dot(col,vec3(0.2126,0.7152,0.0722)); col=max(mix(vec3(gray),col,uSaturation),0.0);
          float lum=max(max(col.r,col.g),col.b); float alpha=clamp(lum,0.0,1.0)*uOpacity;
          fragColor=vec4(col*uOpacity,alpha);
        }\`;

        const buildPalette = (arr) => {
            const p=[];
            for(let i=0;i<MAX_COLORS;i++){ const hex=arr[i]??arr[arr.length-1]; const c=new Color(hex); p.push([c.r,c.g,c.b]); }
            return p;
        };

        let prog;
        function initWebGL(){
            const ctn=document.getElementById('fluid-container'); if(!ctn)return;
            const renderer=new Renderer({alpha:true,premultipliedAlpha:true,antialias:true});
            const gl=renderer.gl; gl.clearColor(0,0,0,0); gl.enable(gl.BLEND); gl.blendFunc(gl.ONE,gl.ONE_MINUS_SRC_ALPHA);
            gl.canvas.style.cssText='position:absolute;top:0;left:0;width:100%;height:100%;display:block;';
            ctn.appendChild(gl.canvas);
            const geometry=new Triangle(gl);
            const colors=['#ff00aa','#ffbb00','#00e5ff'];
            prog=new Program(gl,{vertex:VERT,fragment:FRAG,uniforms:{
                uTime:{value:0}, uResolution:{value:[ctn.offsetWidth,ctn.offsetHeight]},
                uColors:{value:buildPalette(colors)}, uColorCount:{value:colors.length}, uStrandCount:{value:3},
                uSpeed:{value:0.3}, uAmplitude:{value:1.4}, uWaviness:{value:0.8}, uThickness:{value:1.0},
                uGlow:{value:2.0}, uTaper:{value:3.5}, uSpread:{value:0.6}, uHueShift:{value:0},
                uIntensity:{value:0.45}, uOpacity:{value:1.0}, uScale:{value:1.3}, uSaturation:{value:1.2}
            }});
            const mesh=new Mesh(gl,{geometry,program:prog});
            function resize(){ const w=ctn.offsetWidth,h=ctn.offsetHeight; renderer.setSize(w,h); prog.uniforms.uResolution.value=[w,h]; }
            window.addEventListener('resize',resize); resize();
            function update(t){ requestAnimationFrame(update); prog.uniforms.uTime.value=t*0.001; renderer.render({scene:mesh}); }
            requestAnimationFrame(update);
        }

        // smoothly animate fluid uniforms based on playing state
        let targetIntensity=0.45, targetSpeed=0.3, targetGlow=2.0, targetSat=1.2;
        function tweenFluid(){
            if(prog){
                const u=prog.uniforms;
                u.uIntensity.value+=(targetIntensity-u.uIntensity.value)*0.05;
                u.uSpeed.value+=(targetSpeed-u.uSpeed.value)*0.05;
                u.uGlow.value+=(targetGlow-u.uGlow.value)*0.05;
                u.uSaturation.value+=(targetSat-u.uSaturation.value)*0.05;
            }
            requestAnimationFrame(tweenFluid);
        }

        function initScrollAnimations(){
            gsap.registerPlugin(ScrollTrigger);
            const el=document.getElementById('reveal-text'); if(!el)return;
            const text=el.innerText; el.innerHTML='';
            text.split(' ').forEach(word=>{
                const o=document.createElement('span');
                o.style.cssText='overflow:hidden;display:inline-block;vertical-align:bottom;margin-right:0.25em;padding-bottom:0.1em;';
                const inn=document.createElement('span');
                inn.className='reveal-word';
                inn.style.cssText='display:inline-block;transform:translateY(110%);opacity:0;';
                inn.innerText=word; o.appendChild(inn); el.appendChild(o);
            });
            gsap.to('.reveal-word',{y:'0%',opacity:1,duration:0.8,stagger:0.02,ease:'power3.out',
                scrollTrigger:{trigger:el,start:'top 85%',toggleActions:'play none none reverse'}});
        }

        document.addEventListener('DOMContentLoaded',()=>{
            initWebGL();
            tweenFluid();
            initScrollAnimations();

            const input=document.getElementById('reader-input');
            const wc=document.getElementById('word-count');
            const rt=document.getElementById('read-time');
            const timeTotal=document.getElementById('time-total');
            const timeCurrent=document.getElementById('time-current');
            const progressFill=document.getElementById('progress-fill');
            const progressTrack=document.getElementById('progress-track');
            const playBtn=document.getElementById('play-btn');
            const playIcon=document.getElementById('play-icon');
            const statusDot=document.getElementById('status-dot');
            const statusLabel=document.getElementById('status-label');

            let playing=false, progress=0, totalSec=0, speed=1.0, timer=null;

            function fmt(s){ s=Math.max(0,Math.floor(s)); return Math.floor(s/60)+':'+String(s%60).padStart(2,'0'); }

            function updateCounts(){
                const words=input.value.trim().split(/\\s+/).filter(Boolean).length;
                wc.textContent=words+' word'+(words===1?'':'s');
                const mins=words/200;
                rt.textContent='~'+(mins<1?'<1':Math.round(mins))+' min';
                totalSec=Math.max(1, Math.round(words/200*60));
                timeTotal.textContent=fmt(totalSec);
            }
            input.addEventListener('input',updateCounts);
            updateCounts();

            document.getElementById('clear-btn').addEventListener('click',()=>{
                input.value=''; updateCounts(); stop(); progress=0; render();
            });

            function render(){
                progressFill.style.width=(progress*100)+'%';
                timeCurrent.textContent=fmt(progress*totalSec);
            }

            function setActive(active){
                if(active){
                    targetIntensity=0.85; targetSpeed=0.7; targetGlow=2.8; targetSat=1.6;
                    statusDot.style.background='#ff00aa';
                    statusDot.style.boxShadow='0 0 8px #ff00aa';
                    statusLabel.textContent='Speaking…';
                }else{
                    targetIntensity=0.45; targetSpeed=0.3; targetGlow=2.0; targetSat=1.2;
                    statusDot.style.background='#64748b';
                    statusDot.style.boxShadow='none';
                    statusLabel.textContent='Ready to read';
                }
            }

            function play(){
                if(!input.value.trim())return;
                playing=true; playIcon.setAttribute('icon','solar:pause-bold'); setActive(true);
                timer=setInterval(()=>{
                    progress+=(1/totalSec)*0.5*speed;
                    if(progress>=1){ progress=1; stop(); }
                    render();
                },500);
            }
            function stop(){
                playing=false; playIcon.setAttribute('icon','solar:play-bold'); setActive(false);
                if(timer){clearInterval(timer);timer=null;}
            }
            playBtn.addEventListener('click',()=> playing?stop():play());

            progressTrack.addEventListener('click',(e)=>{
                const r=progressTrack.getBoundingClientRect();
                progress=Math.min(1,Math.max(0,(e.clientX-r.left)/r.width)); render();
            });

            // voice dropdown
            const vbtn=document.getElementById('voice-btn');
            const vmenu=document.getElementById('voice-menu');
            const vlabel=document.getElementById('voice-label');
            vbtn.addEventListener('click',(e)=>{e.stopPropagation();vmenu.classList.toggle('hidden');});
            document.querySelectorAll('.voice-opt').forEach(o=>o.addEventListener('click',()=>{
                vlabel.textContent=o.textContent; vmenu.classList.add('hidden');
            }));
            document.addEventListener('click',()=>vmenu.classList.add('hidden'));

            // speed slider
            const sTrack=document.getElementById('speed-track');
            const sFill=document.getElementById('speed-fill');
            const sThumb=document.getElementById('speed-thumb');
            const sLabel=document.getElementById('speed-label');
            let dragging=false;
            function setSpeed(clientX){
                const r=sTrack.getBoundingClientRect();
                let p=Math.min(1,Math.max(0,(clientX-r.left)/r.width));
                speed=0.5+p*1.5; // 0.5x - 2.0x
                sFill.style.width=(p*100)+'%'; sThumb.style.left=(p*100)+'%';
                sLabel.textContent=speed.toFixed(1)+'x';
            }
            sTrack.addEventListener('mousedown',(e)=>{dragging=true;setSpeed(e.clientX);});
            window.addEventListener('mousemove',(e)=>{if(dragging)setSpeed(e.clientX);});
            window.addEventListener('mouseup',()=>dragging=false);
            sTrack.addEventListener('click',(e)=>setSpeed(e.clientX));

            render();
        });
    </script>
</section>`;

  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
