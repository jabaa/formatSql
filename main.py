#!/usr/bin/env python3

import tkinter as tk

keywords = ['SELECT DISTINCT', 'SELECT', 'FROM', 'INNER JOIN', 'ON', 'WITH UR']


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Format SQL")

        self.text = tk.Text(self.root, height=30, width=90)
        self.text.pack()

        self.btn_format = tk.Button(self.root, text='Format', command=self.on_click_format)
        self.btn_format.pack()

        self.btn_cpp_format = tk.Button(self.root, text='C++ Format', command=self.on_click_cpp_format)
        self.btn_cpp_format.pack()

        self.output = tk.Text(self.root, height=30, width=90)
        self.output.pack()

        self.root.mainloop()

    def on_click_format(self):
        text = self.text.get('1.0', 'end').strip()

        formatted = self.format(text)

        self.output.delete('1.0', 'end')
        self.output.insert('end', formatted)

    @staticmethod
    def format(text):
        formatted = ''

        parenthesis = 0

        while len(text) > 0:
            for keyword in keywords:
                if text.startswith(keyword):
                    if text[len(keyword)] == ';':
                        keyword += ';'
                    formatted += keyword + '\n'
                    text = text[len(keyword):].strip()
                    break
            else:
                for pos in range(0, len(text)):
                    subtext = text[pos:]

                    if subtext[0] == '(':
                        parenthesis += 1
                        break
                    if subtext[0] == ')':
                        parenthesis -= 1
                        break
                    if parenthesis != 0:
                        break
                    if subtext[0] == ',':
                        formatted += '  ' + text[:pos+1].strip() + '\n'
                        text = text[pos+1:].strip()
                        break
                    if subtext.startswith('AND') and len(subtext) > 3:
                        formatted += '  ' + text[:pos].strip() + '\n'
                        text = text[pos:].strip()
                        break
                    keyword_found = False
                    for keyword in keywords:
                        if subtext.startswith(keyword):
                            if subtext[len(keyword)] == ';':
                                keyword += ';'
                            formatted += '  ' + text[:pos].strip() + '\n'
                            text = text[pos:].strip()
                            keyword_found = True
                            break
                    if keyword_found:
                        break
                else:
                    formatted += '  ' + text + '\n'
                    text = ''
        return formatted[:-1]

    def on_click_cpp_format(self):
        text = self.text.get('1.0', 'end').strip()

        formatted = self.cpp_format(text)

        self.output.delete('1.0', 'end')
        self.output.insert('end', formatted)

    @staticmethod
    def cpp_format(text):
        formatted = App.format(text)

        pos = 0
        while pos < len(formatted):
            if formatted[pos] == '\n':
                formatted = formatted[:pos] + ' "\n  << "' + formatted[pos+1:]
                pos += 6
            pos += 1
        formatted = 'sqlStatementStrm\n  << "' + formatted + '";'

        return formatted


app = App()
