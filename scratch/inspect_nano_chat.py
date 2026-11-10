with open('assets/js/nano-chat.js', 'r', encoding='utf-8') as f:
    chat_js = f.read()

print("Length of nano-chat.js:", len(chat_js))
print(chat_js[:1200].encode('ascii', 'replace').decode('ascii'))
