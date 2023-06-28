# print("http://www.bvbinfo.com/Season.asp?AssocID=3&Year=2018"[-4:])

# for i in range(4, 8):
#     print(i)
href = "Player=asp?ID=1438"
extracted_text = href.split("=")[-1]
print(extracted_text)
