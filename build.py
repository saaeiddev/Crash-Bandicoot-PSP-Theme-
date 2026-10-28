#!/usr/bin/env python3
"""Build experimental PTF; uses GPL-3.0 PTF Studio sample as template."""
from pathlib import Path
from PIL import Image, ImageOps
import struct,zlib,io
P=Path(__file__).resolve().parent
u16=lambda b,o:struct.unpack_from('<H',b,o)[0]
u32=lambda b,o:struct.unpack_from('<I',b,o)[0]
def block(t,p):
 n=16+len(p); return struct.pack('<HHIII',t,0,n,n,16)+p
def imageblock(t,fmt,order,w,h,bpp,pixels,level):
 b=bytearray(64);struct.pack_into('<HHHHHHHHHH',b,0,0x30,0,fmt,order,w,h,bpp,16,8,2)
 struct.pack_into('<IIII',b,24,0x30,0x40,0x40+len(pixels),0);struct.pack_into('<HHHH',b,40,level,1,3,1);struct.pack_into('<I',b,48,0x40)
 return block(t,bytes(b)+pixels)
def gim(im,indexed=True):
 im=im.convert('RGBA'); w,h=im.size
 if indexed:
  im=im.quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE)
  rgba=im.convert('RGBA'); indices=list(im.getdata()); entries={}
  for i,c in zip(indices,rgba.getdata()):entries[i]=c
  pal=bytearray(1024)
  for i,c in entries.items():pal[i*4:i*4+4]=bytes(c)
  arr=bytes(indices[y*w+x] for ty in range(0,h,8) for tx in range(0,w,16) for y in range(ty,ty+8) for x in range(tx,tx+16) if y<h and x<w)
  blocks=imageblock(5,3,0,256,1,32,pal,2)+imageblock(4,5,1,w,h,8,arr,1)
 else:blocks=imageblock(4,3,0,w,h,32,im.tobytes(),1)
 pic=struct.pack('<HHIII',3,0,16+len(blocks),16,16)+blocks
 root=struct.pack('<HHIII',2,0,16+len(pic),16,16)+pic
 return b'MIG.00.1PSP\0\0\0\0\0'+root
def bmp(im):
 b=io.BytesIO();im.convert('RGB').save(b,format='BMP');return b.getvalue()
def pad(b):return b+b'\0'*(-len(b)%4)
def main():
 raw=(P/'base_sample.ptf').read_bytes(); assert raw[:8]==b'\0PTF\0\1\0\0'
 resources={}
 for group in range(8):
  off=u32(raw,0x100+4*group)
  if not off:continue
  gid,count,size,start=struct.unpack_from('<HHII',raw,off);assert gid==group
  pos=start;items=[]
  for _ in range(count):
   sub,_,typ,comp,size,unpacked=struct.unpack_from('<HHHHII',raw,pos);pos+=32
   data=raw[pos:pos+size];pos+=size;items.append([sub,typ,comp,unpacked,data])
  resources[group]=items
 wall=Image.open(P/'assets/wallpaper/wallpaper.png').convert('RGB')
 mapping={1:'settings',2:'photo',3:'music',4:'video',5:'tv',6:'game',7:'network',8:'extras'}
 if not any(it[0]==5 for it in resources[2]): resources[2].append([5,5,2,0,b''])
 resources[2].sort(key=lambda it:it[0])
 for group,items in resources.items():
  for it in items:
   sub=it[0]; data=None
   if group==1 and sub==0:data=bmp(wall)
   if group==0 and sub==1:data=gim(ImageOps.fit(wall,(300,170)),False)
   if group==0 and sub==0:data=gim(Image.open(P/'assets/category/game.png').resize((16,16),Image.Resampling.LANCZOS))
   if group==2 and sub in mapping:data=gim(Image.open(P/'assets/category'/f'{mapping[sub]}.png'))
   if group in (3,4) and sub%2==0:data=gim(Image.open(P/'assets/subcategory'/f'{group}_{sub:04}.png'))
   if data is not None:
    comp=zlib.compress(data,9);it[2]=2;it[3]=len(data);it[4]=pad(comp)
 out=bytearray(0x120);out[:8]=b'\0PTF\0\1\0\0';out[8:8+len(b'Crash Bandicoot')]=b'Crash Bandicoot';out[136:136+5]=b'CRASH';out[184:188]=b'6.20';out[192:195]=b'0.1';struct.pack_into('<I',out,200,8)
 for g,items in sorted(resources.items()):
  offset=len(out);struct.pack_into('<I',out,0x100+g*4,offset);body=bytearray()
  for sub,typ,comp,unpacked,data in items:
   body+=struct.pack('<HHHHII',sub,0,typ,comp,len(data),unpacked)+bytes(16)+data
  out+=struct.pack('<HHII',g,len(items),len(body),offset+32)+bytes(20)+body
 dest=P/'dist/Crash_Bandicoot_PSP_Theme.ptf';dest.write_bytes(out);print(dest,len(out))
if __name__=='__main__':main()
