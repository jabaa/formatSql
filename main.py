#!/usr/bin/env python3

import tkinter as tk
import sys

keywords = ['SELECT DISTINCT', 'SELECT', 'FROM', 'INNER JOIN', 'ON']

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Format SQL")

        self.text = tk.Text(self.root, height=30, width=90)
        self.text.pack()

        self.btn_format = tk.Button(self.root, text='Format', command=self.format)
        self.btn_format.pack()

        self.output = tk.Text(self.root, height=30, width=90)
        self.output.pack()

        self.root.mainloop()

    def format(self):
        text = self.text.get('1.0', 'end').strip()
        formatted = ''

        parenthesis = 0

        while len(text) > 0:
            for keyword in keywords:
                if text.startswith(keyword):
                    formatted += keyword + '\n'
                    text = text[len(keyword):].strip()
                    break
            else:
                for pos in range(0, len(text)):
                    subtext = text[pos:]
                    print(subtext)
                    if subtext[0] == '(':
                        print('(')
                        parenthesis += 1
                        break
                    if subtext[0] == ')':
                        print(')')
                        parenthesis -= 1
                        break
                    if parenthesis != 0:
                        break
                    if subtext[0] == ',':
                        print(',')
                        formatted += '  ' + text[:pos+1].strip() + '\n'
                        text = text[pos+1:].strip()
                        break
                    if subtext.startswith('AND') and len(subtext) > 3:
                        formatted += '  ' + text[:pos].strip() + '\n'
                        text = text[pos:].strip()
                        break
                    keyword_found = False
                    for keyword in keywords:
                        if text.startswith(keyword):
                            formatted += '  ' + text[:pos].strip() + '\n'
                            text = text[pos:].strip()
                            keyword_found = True
                            break
                    if keyword_found:
                        break
                else:
                    formatted += '  ' + text + '\n'
                    text = ''
        text = text[:-1]

        self.output.delete('1.0', 'end')
        self.output.insert('end', formatted)

app = App()
