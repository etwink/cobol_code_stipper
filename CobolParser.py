import re
from collections import defaultdict

class CobolParser:
    def __init__(self, code: str):
        self.code = code
        self.lines = code.splitlines()
        
        self.divisions = {}
        self.sections = {}
        self.paragraphs = {}
        self.copybooks = []
        self.dependencies = defaultdict(list)
        self.file_operations = defaultdict(list)

    def parse(self):
        self._parse_divisions()
        self._parse_sections_and_paragraphs()
        self._parse_copybooks()
        self._parse_dependencies()
        self._parse_file_ops()
        
        return {
            "divisions": self.divisions,
            "sections": self.sections,
            "paragraphs": self.paragraphs,
            "copybooks": self.copybooks,
            "dependencies": dict(self.dependencies),
            "file_operations": dict(self.file_operations)
        }

    def _parse_divisions(self):
        division_pattern = re.compile(r'^\s*(\w+)\s+DIVISION\.', re.IGNORECASE)
        current_div = None
        buffer = []

        for line in self.lines:
            match = division_pattern.match(line)
            if match:
                if current_div:
                    self.divisions[current_div] = "\n".join(buffer)
                current_div = match.group(1).upper()
                buffer = [line]
            elif current_div:
                buffer.append(line)

        if current_div:
            self.divisions[current_div] = "\n".join(buffer)

    def _parse_sections_and_paragraphs(self):
        section_pattern = re.compile(r'^\s*(\w[\w-]*)\s+SECTION\.', re.IGNORECASE)
        paragraph_pattern = re.compile(r'^\s*(\w[\w-]*)\.\s*$', re.IGNORECASE)

        current_section = None
        current_paragraph = None
        buffer = []

        for line in self.lines:
            section_match = section_pattern.match(line)
            paragraph_match = paragraph_pattern.match(line)

            if section_match:
                current_section = section_match.group(1).upper()
                self.sections[current_section] = []
                current_paragraph = None

            elif paragraph_match:
                if current_paragraph:
                    self.paragraphs[current_paragraph] = "\n".join(buffer)
                    buffer = []

                current_paragraph = paragraph_match.group(1).upper()
                self.paragraphs[current_paragraph] = ""
                if current_section:
                    self.sections[current_section].append(current_paragraph)

            if current_paragraph:
                buffer.append(line)

        if current_paragraph:
            self.paragraphs[current_paragraph] = "\n".join(buffer)

    def _parse_copybooks(self):
        copy_pattern = re.compile(r'\bCOPY\s+(\w+)', re.IGNORECASE)
        for line in self.lines:
            match = copy_pattern.search(line)
            if match:
                self.copybooks.append(match.group(1).upper())

    def _parse_dependencies(self):
        perform_pattern = re.compile(r'\bPERFORM\s+(\w[\w-]*)', re.IGNORECASE)
        call_pattern = re.compile(r"\bCALL\s+'?(\w+)'?", re.IGNORECASE)

        for para_name, para_code in self.paragraphs.items():
            for perform in perform_pattern.findall(para_code):
                self.dependencies[para_name].append({
                    "type": "PERFORM",
                    "target": perform.upper()
                })

            for call in call_pattern.findall(para_code):
                self.dependencies[para_name].append({
                    "type": "CALL",
                    "target": call.upper()
                })

    def _parse_file_ops(self):
        file_pattern = re.compile(r'\b(READ|WRITE|OPEN|CLOSE)\s+(\w+)', re.IGNORECASE)

        for para_name, para_code in self.paragraphs.items():
            for match in file_pattern.findall(para_code):
                op, target = match
                self.file_operations[para_name].append({
                    "operation": op.upper(),
                    "target": target.upper()
                })
