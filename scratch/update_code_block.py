with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """                    <div class="code-block-visual">
                        <code>
                            <span class="keyword">const</span> <span class="var">skills</span> = [<br>
                            &nbsp;&nbsp;<span class="keyword">'Bilingual/Native-level English'</span>,<br>
                            &nbsp;&nbsp;<span class="keyword">'Python & JavaScript'</span>,<br>
                            &nbsp;&nbsp;<span class="keyword">'Data Analysis'</span>,<br>
                            &nbsp;&nbsp;<span class="keyword">'Full-stack Development'</span>,<br>
                            &nbsp;&nbsp;<span class="keyword">'Team working'</span>,<br>
                            &nbsp;&nbsp;<span class="keyword">'Vertex AI'</span>,<br>
                            &nbsp;&nbsp;<span class="keyword">'LLM Fine-tuning'</span>,<br>
                            &nbsp;&nbsp;<span class="keyword">'Cloud Architecture'</span><br>
                            ];
                        </code>
                    </div>"""

replacement = """                    <div class="code-block-visual">
                        <code>
                            <span class="drone-code-line"><span class="keyword">const</span> <span class="var">skills</span> = [</span>
                            <span class="drone-code-line">&nbsp;&nbsp;<span class="keyword">'Bilingual/Native-level English'</span>,</span>
                            <span class="drone-code-line">&nbsp;&nbsp;<span class="keyword">'Python &amp; JavaScript'</span>,</span>
                            <span class="drone-code-line">&nbsp;&nbsp;<span class="keyword">'Data Analysis'</span>,</span>
                            <span class="drone-code-line">&nbsp;&nbsp;<span class="keyword">'Full-stack Development'</span>,</span>
                            <span class="drone-code-line">&nbsp;&nbsp;<span class="keyword">'Team working'</span>,</span>
                            <span class="drone-code-line">&nbsp;&nbsp;<span class="keyword">'Vertex AI'</span>,</span>
                            <span class="drone-code-line">&nbsp;&nbsp;<span class="keyword">'LLM Fine-tuning'</span>,</span>
                            <span class="drone-code-line">&nbsp;&nbsp;<span class="keyword">'Cloud Architecture'</span></span>
                            <span class="drone-code-line">];</span>
                        </code>
                    </div>"""

assert target in content, "target not found"
content = content.replace(target, replacement, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated code-block-visual in index.html!")
