import numpy as np, math, sys
from numba import njit, prange
from PIL import Image, ImageFilter

PROF=np.array([(0,0),(0.66,0),(0.66,0.07),(0.6,0.11),(0.62,0.15),(0.54,0.21),(0.44,0.25),(0.4,0.3),
 (0.31,0.5),(0.25,0.9),(0.21,1.18),(0.32,1.22),(0.34,1.27),(0.24,1.31),(0.22,1.35),(0.31,1.39),
 (0.36,1.44),(0.27,1.58),(0.33,1.64),(0.31,1.69),(0.0,1.71)],dtype=np.float64)

@njit(cache=True)
def sdpoly(px,py):
    n=PROF.shape[0]
    d=(px-PROF[0,0])**2+(py-PROF[0,1])**2; s=1.0
    j=n-1
    for i in range(n):
        ex=PROF[j,0]-PROF[i,0]; ey=PROF[j,1]-PROF[i,1]
        wx=px-PROF[i,0]; wy=py-PROF[i,1]
        t=(wx*ex+wy*ey)/(ex*ex+ey*ey); t=min(1.0,max(0.0,t))
        bx=wx-ex*t; by=wy-ey*t; dd=bx*bx+by*by
        if dd<d: d=dd
        c1=py>=PROF[i,1]; c2=py<PROF[j,1]; c3=ex*wy>ey*wx
        if (c1 and c2 and c3) or ((not c1) and (not c2) and (not c3)): s=-s
        j=i
    return s*math.sqrt(d)

@njit(cache=True)
def sdbox(x,y,z,bx,by,bz,r):
    qx=abs(x)-bx+r; qy=abs(y)-by+r; qz=abs(z)-bz+r
    o=math.sqrt(max(qx,0)**2+max(qy,0)**2+max(qz,0)**2)
    return o+min(max(qx,max(qy,qz)),0.0)-r

@njit(cache=True)
def smin(a,b,k):
    h=max(k-abs(a-b),0.0)/k
    return min(a,b)-h*h*k*0.25

@njit(cache=True)
def king(x,y,z):
    r=math.sqrt(x*x+z*z)
    # crown notches: modulate radius near top
    d=sdpoly(r,y)-0.012
    if y>1.5:
        a=math.atan2(z,x); d+= 0.02*max(0.0,math.cos(8*a))*min(1.0,(y-1.5)*6)
    c=sdbox(x,y-1.86,z,0.055,0.16,0.055,0.015)
    c=min(c,sdbox(x,y-1.9,z,0.15,0.05,0.055,0.015))
    return smin(d,c,0.04)

@njit(cache=True)
def pawn(x,y,z):
    # fallen pawn lying on floor, axis along x, placed back-right
    px=x-1.35; py=y-0.36; pz=z-1.6
    ca=math.cos(0.6); sa=math.sin(0.6)
    rx=ca*px-sa*pz; rz=sa*px+ca*pz
    # pawn axis along rx; local height h=rx+0.55
    h=rx+0.55; rr=math.sqrt(py*py+rz*rz)
    body=math.sqrt(max(rr-0.36+0.45*h*0.4,0)**2)  # placeholder
    d1=max(math.sqrt(py*py+rz*rz)-(0.36-0.18*min(max(h,0),1.0)),abs(h-0.45)-0.45)
    d2=math.sqrt((h-1.08)**2+py*py+rz*rz)-0.22
    return smin(d1,d2,0.08)

@njit(cache=True)
def scene(x,y,z):
    k=king(x,y,z); p=1e9; f=y
    if k<p and k<f: return k,1
    if p<f: return p,2
    return f,0

@njit(cache=True)
def march(ox,oy,oz,dx,dy,dz,tmax):
    t=0.01
    for i in range(220):
        d,m=scene(ox+dx*t,oy+dy*t,oz+dz*t)
        if d<0.0006*t: return t,m
        t+=d*0.9
        if t>tmax: break
    return -1.0,-1

@njit(cache=True)
def normal(x,y,z):
    e=0.0015
    a,_=scene(x+e,y,z); b,_=scene(x-e,y,z); c,_=scene(x,y+e,z); d,_=scene(x,y-e,z); f,_=scene(x,y,z+e); g,_=scene(x,y,z-e)
    nx=a-b; ny=c-d; nz=f-g; l=math.sqrt(nx*nx+ny*ny+nz*nz)
    return nx/l,ny/l,nz/l

@njit(cache=True)
def env(dx,dy,dz):
    # gold softbox back-left, white strip right, dark otherwise
    r=0.004; g=0.003; b=0.006
    # key softbox direction
    kx,ky,kz=-0.55,0.45,0.70; l=math.sqrt(kx*kx+ky*ky+kz*kz); kx/=l;ky/=l;kz/=l
    c=dx*kx+dy*ky+dz*kz
    if c>0: s=c**60*14.0+c**8*0.35; r+=s*1.0; g+=s*0.62; b+=s*0.22
    # right white strip (vertical)
    sx,sz=0.85,-0.2
    cc=dx*sx+dz*sz
    if cc>0.82 and dy>-0.1 and dy<0.8: w=(cc-0.82)*25; r+=w*0.9; g+=w*0.95; b+=w*1.1
    # top fill
    if dy>0.9: q=(dy-0.9)*3; r+=q*0.3; g+=q*0.25; b+=q*0.2
    return r,g,b

@njit(cache=True)
def softshadow(ox,oy,oz,dx,dy,dz):
    res=1.0; t=0.02
    for i in range(64):
        d=king(ox+dx*t,oy+dy*t,oz+dz*t)
        res=min(res,10*d/t)
        if res<0.001: return 0.0
        t+=max(d,0.01)
        if t>6: break
    return max(res,0.0)

@njit(cache=True)
def shade_obj(px,py,pz,dx,dy,dz,m):
    nx,ny,nz=normal(px,py,pz)
    vd=-(dx*nx+dy*ny+dz*nz)
    f0=0.04 if m==1 else 0.06
    fr=f0+(1-f0)*(1-max(vd,0.0))**5
    rdx=dx-2*nx*(dx*nx+dy*ny+dz*nz); rdy=dy-2*ny*(dx*nx+dy*ny+dz*nz); rdz=dz-2*nz*(dx*nx+dy*ny+dz*nz)
    er,eg,eb=env(rdx,rdy,rdz)
    if rdy<0: er*=0.15;eg*=0.15;eb*=0.15
    spec=fr*1.0+0.06
    base=0.012 if m==1 else 0.5
    # diffuse from key
    kx,ky,kz=-0.55,0.45,0.70; l=math.sqrt(kx*kx+ky*ky+kz*kz); kx/=l;ky/=l;kz/=l
    dif=max(nx*kx+ny*ky+nz*kz,0.0)
    if m==2: dif*=softshadow(px+nx*0.01,py+ny*0.01,pz+nz*0.01,kx,ky,kz)
    cr=base*dif*1.0*(1.0 if m==1 else 0.9); cg=base*dif*(0.62 if m==1 else 0.8); cb=base*dif*(0.25 if m==1 else 0.7)
    if m==2: cr*=0.25;cg*=0.25;cb*=0.25
    sp=max(ny,0.0)**6*0.10
    return cr+er*spec+sp*0.9*fr*4, cg+eg*spec+sp*0.85*fr*4, cb+eb*spec+sp*0.75*fr*4

@njit(parallel=True,cache=True)
def render(W,H,ss):
    img=np.zeros((H,W,3))
    cx,cy,cz=0.0,1.25,-4.0
    tx,ty,tz=0.0,0.95,0.0
    fx,fy,fz=tx-cx,ty-cy,tz-cz; l=math.sqrt(fx*fx+fy*fy+fz*fz); fx/=l;fy/=l;fz/=l
    rx,ry,rz=fz,0.0,-fx; l=math.sqrt(rx*rx+rz*rz); rx/=l;rz/=l
    ux=-(ry*fz-rz*fy); uy=-(rz*fx-rx*fz); uz=-(rx*fy-ry*fx)
    fov=2.45
    for j in prange(H):
        for i in range(W):
            acc0=0.0;acc1=0.0;acc2=0.0
            for sj in range(ss):
                for si in range(ss):
                    u=((i+(si+0.5)/ss)/W*2-1); v=-((j+(sj+0.5)/ss)/H*2-1)
                    dx=fx*fov+rx*u+ux*v; dy=fy*fov+ry*u+uy*v; dz=fz*fov+rz*u+uz*v
                    l=math.sqrt(dx*dx+dy*dy+dz*dz); dx/=l;dy/=l;dz/=l
                    t,m=march(cx,cy,cz,dx,dy,dz,30.0)
                    r=0.0;g=0.0;b=0.0
                    if m>=1:
                        px=cx+dx*t;py=cy+dy*t;pz=cz+dz*t
                        r,g,b=shade_obj(px,py,pz,dx,dy,dz,m)
                    elif m==0:
                        px=cx+dx*t;py=cy+dy*t;pz=cz+dz*t
                        # glossy floor: reflection of scene
                        rdx,rdy,rdz=dx,-dy,dz
                        fr=0.03+0.97*(1-abs(dy))**5
                        t2,m2=march(px,0.002,pz,rdx,rdy,rdz,12.0)
                        rr=0.0;rg=0.0;rb=0.0
                        if m2>=1:
                            rr,rg,rb=shade_obj(px+rdx*t2,0.002+rdy*t2,pz+rdz*t2,rdx,rdy,rdz,m2)
                            att=math.exp(-t2*0.9); rr*=att;rg*=att;rb*=att
                        sh=softshadow(px,0.002,pz,-0.55/1.0,0.45,0.70)
                        # warm pool of light on floor
                        dist=math.sqrt((px+0.4)**2+(pz-0.2)**2)
                        pool=0.03*math.exp(-dist*dist*0.8)+0.05*math.exp(-(px*px+pz*pz)*1.6)*(0.25+0.75*sh)
                        r=rr*(fr*0.9+0.25)+pool*1.0; g=rg*(fr*0.9+0.25)+pool*0.62; b=rb*(fr*0.9+0.25)+pool*0.3
                        fog=math.exp(-max(t-3.2,0)*1.4)
                        hx=u+0.25; hy=v-0.25; hz=math.exp(-(hx*hx+hy*hy)*2.2)
                        r=r*fog+(1-fog)*(0.001+hz*0.018); g=g*fog+(1-fog)*(0.001+hz*0.011); b=b*fog+(1-fog)*(0.002+hz*0.007)
                    else:
                        # background haze glow behind king, upper-left warm
                        hx=u+0.25; hy=v-0.25
                        hz=math.exp(-(hx*hx+hy*hy)*2.2)
                        r=0.001+hz*0.018; g=0.001+hz*0.011; b=0.002+hz*0.007
                    tend=t if t>0 else 12.0
                    vol=0.0
                    for k in range(40):
                        tt=tend*(k+0.5)/40
                        qx=cx+dx*tt; qy=cy+dy*tt; qz=cz+dz*tt
                        if qy<0: continue
                        h=4.6-qy
                        rad=math.sqrt(qx*qx+qz*qz)
                        cone=h*0.30
                        if rad<cone:
                            vol+=(1-(rad/cone)**2)*math.exp(-h*0.25)*tend/40
                    r+=vol*0.030; g+=vol*0.026; b+=vol*0.020
                    acc0+=r;acc1+=g;acc2+=b
            n=ss*ss
            img[j,i,0]=acc0/n; img[j,i,1]=acc1/n; img[j,i,2]=acc2/n
    return img

W=int(sys.argv[1]) if len(sys.argv)>1 else 360
ss=int(sys.argv[2]) if len(sys.argv)>2 else 1
img=render(W,W,ss)
np.save('hdr.npy',img)
print('done',img.max(),img.mean())
