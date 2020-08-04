import sumy
import numpy as np
import wx
import logging

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


# Set up logging config
logging.basicConfig(filename='doc_summarizer_log.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

LANGUAGE = "english"
stemmer = Stemmer(LANGUAGE)

class MyFrame(wx.Frame):
    def __init__(self, parent: wx.Frame, title: str, size: int):
        super(MyFrame, self).__init__(parent, title=title, size=size)
        self.panel = MyPanel(self)


class MyPanel(wx.Panel):
    def __init__(self, parent: wx.Frame):
        super(MyPanel, self).__init__(parent)

        # Title
        self.lbl_title = wx.StaticText(self, label="Document Summarizer", pos=(10, 10))
        self.lbl_title.SetFont(wx.Font(18, wx.DECORATIVE, wx.NORMAL, wx.BOLD))

        # File Selection
        self.lbl_choose_file = wx.StaticText(self, label="Choose a file to summarize...", pos=(20, 50))
        self.btn_choose_file = wx.Button(self, label="Select File", pos=(20, 75))
        self.btn_choose_file.Bind(wx.EVT_BUTTON, self.on_click_select)

        # Summary
        self.lbl_summary = wx.StaticText(self, label="Generated Summary:", pos=(250, 50))
        self.txtctrl_summary = wx.TextCtrl(self, pos=(250, 75), size=(300, 300),
                                           style=wx.TE_MULTILINE | wx.TE_READONLY,
                                           value="Your summary will appear here...")
        self.btn_summarize = wx.Button(self, label="Summarize", pos=(300, 385))
        self.btn_summarize.Bind(wx.EVT_BUTTON, self.on_click_summarize)
        self.btn_save = wx.Button(self, label="Save Summary", pos=(400, 385))
        self.btn_save.Bind(wx.EVT_BUTTON, self.on_click_save)
        self.btn_save.Disable()

        # Settings
        self.lbl_settings = wx.StaticText(self, label="Settings:", pos=(20, 125))
        self.stbox_settings = wx.StaticBox(self, pos=(20, 140), size=(200,236))
        self.rbox_algo_options = wx.RadioBox(self, label="Summarizer", pos=(35, 160),
                                             style=wx.RA_SPECIFY_COLS, majorDimension=1,
                                             choices=["LexRank", "TextRank", "Luhn", "LSA", "SumBasic"])
        self.Bind(wx.EVT_RADIOBOX, self.on_radio_button_select)

        self.lbl_title = wx.StaticText(self, label="Sentences:", pos=(35, 320))

        self.spnctrl_sentences = wx.SpinCtrl(self, min=1, initial=5, style=wx.SP_ARROW_KEYS, pos=(35, 340))
        self.Bind(wx.EVT_SPINCTRL, self.on_sentences_changed)

        # Initialize

        self.file = None
        self.summarizer = None

        self.summarizer_str = self.rbox_algo_options.GetString(self.rbox_algo_options.GetSelection())
        self.choose_summarizer(self.summarizer_str)
        self.sentences = self.spnctrl_sentences.GetValue()

        logging.debug("Panel successfuly initialized")
        logging.debug("Initial Summarizer:{}".format(self.summarizer_str))
        logging.debug("Initial Sentences:{}".format(self.sentences))

        #print("Summarizer is", self.summarizer_str)
        #print("Sentences:", self.sentences)

    # Summarize Selected File with Selected Settings
    def on_click_summarize(self, event: wx.EVT_BUTTON):
        logging.debug("Summarize Button Clicked!")
        if self.file is None:
            logging.debug("NO FILE SELECTED")
            md_no_file = wx.MessageDialog(self, caption="Warning!",
                             message="You have not selected a file to summarize.\nPlease select a file and try again.",
                             style=wx.OK)
            md_no_file.ShowModal()
        else:
            logging.debug("SELECTED FILE:{}".format(self.file))
            parser = PlaintextParser.from_file(self.file, Tokenizer(LANGUAGE))
            summary = self.summarizer(parser.document, self.sentences)
            full_summary = ""
            for sentence in summary:
                full_summary += str(sentence) + "\n\n"
            self.txtctrl_summary.SetValue(full_summary)
            logging.debug("GENERATED SUMMARY FOR {}:\n{}".format(self.file, full_summary))
            self.btn_save.Enable()

    # Change number of sentences summary will be
    def on_sentences_changed(self, event):
        self.sentences = self.spnctrl_sentences.GetValue()
        logging.debug("Number of Sentences changed to: {}".format(self.sentences))
        # print("Sentences Changed to:", self.sentences)

    # Change summarizer type
    def on_radio_button_select(self, event):
        self.summarizer_str = self.rbox_algo_options.GetString(self.rbox_algo_options.GetSelection())
        # print("Summarizer changed to", self.summarizer_str)
        self.choose_summarizer(self.summarizer_str)
        logging.debug("Summarizer successfully changed to: {}".format(self.summarizer_str))

    # Create new summarizer based on selected radio button choice
    def choose_summarizer(self, summarizer_string: str):
        logging.debug("Changing summarizer to: {}".format(summarizer_string))
        if summarizer_string == "LexRank":  # LexRank
            self.summarizer = LexRankSummarizer(stemmer)

        elif summarizer_string == "TextRank":  # TextRank
            self.summarizer = TextRankSummarizer(stemmer)

        elif summarizer_string == "Luhn":  # Luhn
            self.summarizer = LuhnSummarizer(stemmer)

        elif summarizer_string == "LSA":  # LSA
            self.summarizer = LsaSummarizer(stemmer)

        elif summarizer_string == "SumBasic":  # SumBasic
            self.summarizer = SumBasicSummarizer(stemmer)

        # allow summarizer to take stop words into account
        self.summarizer.stop_words = get_stop_words(LANGUAGE)

    # Open file dialog so user can elect file to summarize
    def on_click_select(self, event: wx.EVT_BUTTON):
        logging.debug("Select File Button Clicked!")
        with wx.FileDialog(self, "Open TXT file", wildcard="TXT files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                logging.debug("USER CANCELED OPEN FILE OPERATION")
                return  # the user changed their mind
            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            filename = fileDialog.GetFilename()

            try:
                # save selected file path
                with open(pathname, 'r') as file:
                    self.file = pathname

                self.lbl_choose_file.SetLabelText("Selected: {}".format(filename))
                self.txtctrl_summary.SetValue("Your summary will appear here...")
                self.btn_save.Disable()
                logging.debug("New File Selected: {}".format(pathname))

            except IOError:
                wx.LogError("Cannot open file '%s'." % pathname)

    # Save generated summary to text file
    def on_click_save(self, event: wx.EVT_BUTTON):
        logging.debug("Save Summary Button Clicked!")
        with wx.FileDialog(self, "Save Summary", wildcard="TXT files (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                logging.debug("USER CANCELED SAVE FILE OPERATION")
                return  # the user changed their mind

                # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    file.write(self.txtctrl_summary.GetValue())
                    logging.debug("Summary saved to:{}".format(pathname))
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(parent=None, title="Document Summarizer", size=(600, 480))
        self.frame.SetMinSize(size=(600,480))
        self.frame.Show()
        return True


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()



