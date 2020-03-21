import numpy as np

path = '/home/manuela/Uni/jaar_1_Master/Natural_Computing/negative-selection/syscalls/snd-cert/'

def make_chunks(string, length):
    chunks = []
    for i in range(len(string)):
        if i+length < len(string):
            chunks.append(string[i:i+length])
        else:
            return chunks

def preprocessing(filename):

    file = open(path+filename, 'r')
    chunks = []
    line_nr = []
    for nr, line in enumerate(file):
        substrings = make_chunks(line,7)
        line_nr.append([nr for x in substrings])
        chunks.extend(substrings)

    file.close()
    file = open(path+'Preprocessed/'+filename+'.p','w+')
    for chunk in chunks:
        file.write(chunk+'\n')
    file.close()

    file = open(path+'Preprocessed/'+filename+'.chunklen','w+')
    for nr in line_nr:
        file.write(str(len(nr))+'\n')
    file.close()

def postprocessing(nr, r):
    chunk_length = np.loadtxt(path+'Preprocessed/'+'snd-cert.'+nr+'.test.chunklen')
    pred = np.loadtxt('syscalls_out'+r+'/snd-cert.'+nr+'.test.out')
    new_pred = []
    i = 0
    for chunk_l in chunk_length:
        chunk_l = int(chunk_l)
        #print(chunk_l)
        p = pred[i:i+chunk_l]
        #print(p)
        p = p.sum()
        new_pred.append(p/chunk_l)
        i = i+chunk_l
        #print(i)
        #print()
    
    file = open('syscalls_out'+r+'/snd-cert.'+nr+'.test.out.p','w+')
    for chunk in new_pred:
        file.write(str(chunk)+'\n')
    file.close()
    #print(len(pred))

#filenames = ['snd-cert.train', 'snd-cert.1.test', 'snd-cert.2.test', 'snd-cert.3.test']
#for filename in filenames:
#    preprocessing(filename)

for i in range(1,3):
    postprocessing(str(i),str(4))
