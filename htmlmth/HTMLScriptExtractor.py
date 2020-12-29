from HTMLParser import HTMLParser


class HTMLScriptExtractor(HTMLParser):

    def reset(self):
        HTMLParser.reset(self)
        self.full_rawdata = ""
        self.scripts = []
        self.handling_script_tag = False

    def feed(self, data):
        HTMLParser.feed(self, data)
        self.full_rawdata += data

    @property
    def chunks(self):
        chunks = []
        data = self.full_rawdata

        for script in self.scripts:
            index = data.find(script)
            chunk = data[:index]
            chunks.append(chunk)
            chunks.append(script)
            data = data[index+len(script):]
        chunks.append(data)

        return chunks

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.handling_script_tag = True

    def handle_endtag(self, tag):
        if tag == "script":
            self.handling_script_tag = False

    def handle_data(self, data):
        # todo: ensure data always contains the full script data contents
        if self.handling_script_tag:
            self.scripts.append(data)
