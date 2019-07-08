# Bilingual-ebook-maker
I created this script in order to create automatically bilingual ebooks from two ebooks in different languages.
Bilingual ebook with one paragraph in one language, then the other in another language. Those kind of books are great to learn a foreign language.

This task which seems easy is not so because different translations of the same book usually don't have exactly the same paragraphs and inner fb2 settings may not be arranged the same way.

The main principle is that books can be considered as binary strings if you say that dialogs are 1 and paragraphs are 0.
The script try to match the 2 binary strings as well as possible. It's not perfect but you can improve it maybe. On my test you get about 80-90% of the book matched correctly.

The script is a mess, partly in french and without much comments. Sorry about that.

Requisit : ebooks should be .FB2 format. Have python installed.

Step 1 : Books file names should be set in the script line 380 : 

texteA = ouvrelelivre("garri.fb2") #grosse str
texteB = ouvrelelivre("harry.fb2")#grosse str

Step 2 : Put the ebook files in same folder than the script.

Step 3 : Run the script.

Step 4 : hopefully it worked!

Note you have the files LivreDesScores.txt and LivreDesScores2.txt which gives you some feedback on the process.

Enjoy.
