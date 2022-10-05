import time

encoded_text = open("encoded_text.txt").read()
from code import Decoder
d = Decoder(encoded_text)
tic = time.clock()
decoded_text = d.decode()
toc = time.clock()
if (toc - tic > 60):
    print("time is ", int((toc - tic)/60), ":", int((toc - tic)%60))
else:
    print("time is ", (toc - tic))
print(decoded_text)