# -*- coding: utf-8 -*-
"""
@author: Rushikesh
"""

#Please enter the Directory_Name when you call the function. The directory names contains the poitive files and the negative files. Run each separately in different files.

import os
import re
from tika import parser
from collections import OrderedDict



def Data_Cleaning(Directory_Name):
    directory = os.chdir(Directory_Name)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

       

        if filename.endswith(".pdf"): 
                #filename = 'IRAS #5 Hammond.pdf'
                raw = parser.from_file(filename)
                df = (raw["content"])
                df= df.strip("\n")
                df = df.lstrip("\n")
                df=df.rstrip("\n")
                df=df.replace("\n", " ")
                df = df.encode('ascii', 'ignore')
                df = str(df, 'utf-8')
                 
                patt = re.compile('(\s*)\U0000F0B7(\s*)')
                df = patt.sub(' ', df)
                df = re.sub(r'^https?:\/\/.*[\r\n]*', '', df, flags=re.MULTILINE)
                df = re.sub(r'^http?:\/\/.*[\r\n]*', '', df, flags=re.MULTILINE)
                df = re.sub(r'^www?:\/\/.*[\r\n]*', '', df, flags=re.MULTILINE)
                df= ''.join(c for c in df if c not in "(){}?\;:_+=^&*%$#@!~`|")
                df = df.replace("\"", "")
                df = df.replace("/", " ")
                df = df.replace("-", " ")
     
                df = re.sub(r'\b[A-Z]+\b','', df)
                df = re.sub("\d+\.\d+",'', df)
                df = " ".join(df.split())
                
#------------------------- Keyword Matching - Media --------------------------------------------------------------------------------------------------------------------------------

    #5. Indoor Air
                list27 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('• ') or df.split('.” ')) if ('indoor air') in sentence]
    #6. Groundwater
                list1 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ')  or df.split('.” ')) if ('ground water') in sentence]
                list2 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('groundwater') in sentence]
                list3 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ')  or df.split('.” ')) if ('Groundwater') in sentence]
                list28 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ')  or df.split('.” ')) if ('Ground water') in sentence]
    #7. Within 15 or 30 feet
                list4 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('within 15 feet') in sentence]
                list5 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('within fifteen feet') in sentence]
                list6 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('within 30 feet') in sentence]
                list7 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('within thirty feet') in sentence]
                list8 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('Within fifteen feet') in sentence]
                list9 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('Within thirty feet') in sentence]
                list10 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ("<15'") in sentence]
                list11= [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ("<30'") in sentence]
    #8. Resident or commercial air}
                list12 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('residential air') in sentence]
                list13 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('commercial air') in sentence]
    #9. Soil gas
                list14 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('soil gas') in sentence]
    #10. Testing private residential municipal generic terms - Looks good
                list15 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('private') in sentence]
                list16 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('residential') in sentence]
                list17 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('public') in sentence]
                list18 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('municipal') in sentence]
    #11. Critical Pathway exposure
                list19 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('critical exposure pathway') in sentence]
    #12. NAPL
                list21 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('Nonaqueous') in sentence]
                list22 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('NAPL') in sentence]
                list23 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('LNAPL') in sentence]
                list24 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('Non-aqueous') in sentence]
                list25 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('nonaqueous') in sentence]
                list26 = [sentence + '. ' for sentence in (df.split('. ') or df.split('; ') or df.split('.” ')) if ('non-aqueous') in sentence]
    #13. Bringing all together. Removing duplicate sentences and adding it to the corpus.
                final_corpus = list1 + list2 + list3 + list4 + list5 + list6 +list7 + list8+ list10 + list11 + list12 + list13 + list14 + list15 + list16 + list17 + list18 +list19 +list21+list22 + list23+list24+list25 +list26 + list27 + list28
                final_corpus =  list(OrderedDict.fromkeys(final_corpus))
                str1 = ''.join(final_corpus)
                str1 = re.sub(',', ' ', str1)

    #14. Removing Addresses
                address_pat = re.compile(r'\d{1,4} [\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd)\W?(?=\s|$)',re.IGNORECASE)
                str1 = address_pat.sub(' ', str1)
    #15. Removing dates and alpha numeric characters and removing <

                date_1 = re.compile('\d{2}/\d{2}/\d{4}')
                str1 = date_1.sub(' ', str1)
                date_3 = re.compile('[A-Z][a-z]{0,10}\s\d{0,2}\s\d{4}',re.IGNORECASE)
                str1 = date_3.sub(' ', str1)
                date_3 = re.compile('[A-Z][a-z]{0,10}\s\d{4}',re.IGNORECASE)
                str1 = date_3.sub(' ', str1)
                new_s = ""
                for word in str1.split(' '):
                                if any(char.isdigit() for char in word) and any(c.isalpha() for c in word):
                                    new_s += ''.join([i for i in word if not i.isdigit()])
                                else:
                                    new_s += word
                                new_s += ' '
                str1 = new_s
                str1 = str1.replace('–', ' ')
                str1 = str1.replace('<', '')
                str1 = re.sub(r'\b[A-Z]+\b','', str1)
                str1 = " ".join(str1.split())

    #16. Remove numbers from String

                str1 = ''.join([i for i in str1 if not i.isdigit()])
                str1 = " ".join(str1.split())

    #24. Remove 2 lettered words

                shortword = re.compile(r'\W*\b\w{1,2}\b')
                str1 = shortword.sub('', str1)

# ------------------------- Keyword Matching- Flagwords ------------------------------------------------------------------------------------------------------------------------------------------------------------
                
    #17. Impact keyword

                list1 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('• ') or str1.split('.” ')) if ('impact') in sentence]
    #18. NAPL

                list2 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('.” ')) if ('Nonaqueous') in sentence]
                list3 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('.” ')) if ('NAPL') in sentence]
                list4 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('.” ')) if ('LNAPL') in sentence]
                list5 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('.” ')) if ('Non-aqueous') in sentence]
                list6 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('• ') or str1.split('.” ')) if ('non-aqueous') in sentence]

    #19. Affect
                list7 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('.” ')) if ('affect') in sentence]
                list8 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('.” ')) if ('Affect') in sentence]
    #20. Contaminate
                list9 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('.” ')) if ('contaminat') in sentence]
    #21. Pollute
                list10 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('• ') or str1.split('.” ')) if ('pollut') in sentence]
    #22. Exceed
                list11 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('.” ')) if ('exceed') in sentence]

    #23. Hazard
                list12 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('• ') or str1.split('.” ')) if ('hazard') in sentence]
                list13 = [sentence + '. ' for sentence in (str1.split('. ') or str1.split('; ') or str1.split('.') or str1.split(' .') or str1.split('• ') or str1.split('.” ')) if ('nonaqueous') in sentence]

    #Bringing it all together and then merging the corpus

                final_corpus = list1 + list2 + list3 + list4 + list5 + list6 +list7 + list8 + list9 + list10 + list11 + list12 + list13
                final_corpus =  list(OrderedDict.fromkeys(final_corpus))
                str2 = ' '.join(final_corpus)

    #Generating output in txt format

                output = open('out_{0}.txt'.format(filename), 'wb')
                output.write(str(str2).encode("utf-8"))
                output.close()