import sys
import gtk

from firstboot.config import *
from firstboot.constants import *
from firstboot.functions import *
from firstboot.module import *
from firstboot.module import Module

import gettext
_ = lambda x: gettext.ldgettext("firstboot", x)

sys.path.append("/usr/share/rhsm")
from gui import managergui

class moduleClass(Module,managergui.RegisterScreen):
    def __init__(self):
        """
        Create a new firstboot Module for the 'register' screen.
        """
        Module.__init__(self)
        managergui.create_and_set_basic_connection()
        self.priority = 50    #this value is relative to when you want to load the screen
                              # so check other modules before setting
        self.sidebarTitle = _("Entitlement Registration")
        self.title = _("Entitlement Platform Registration")

    def apply(self, interface, testing=False):
        """
        'Next' button has been clicked - try to register with the
        provided user credentials and return the appropriate result
        value.
        """
        valid_registration = self.register(testing=testing)

        if valid_registration:
            return RESULT_SUCCESS
        else:
            return RESULT_FAILURE

    def close_window(self):
        """
        Overridden from RegisterScreen - we want to bypass the default behavior
        of hiding the GTK window.
        """
        pass

    def emit_consumer_signal(self):
        """
        Overriden from RegisterScreen - we don't care about consumer update signals.
        """
        pass

    def registrationTokenScreen(self):
        """
        Overridden from RegisterScreen - ignore any requests to show the registration
        screen on this particular page.
        """
        pass

    def createScreen(self):
        """
        Create a new instance of gtk.VBox, pulling in child widgets from the glade file.
        """
        self.vbox = gtk.VBox(spacing=10)
        self.register_dialog = managergui.rhsm_xml.get_widget("dialog-vbox3")
        self.register_dialog.reparent(self.vbox)

        # Get ride of the 'register' and 'cancel' buttons, as we are going to use
        # the 'forward' and 'back' buttons provided by the firsboot module to drive
        # the same functionality
        self._destroy_widget('register_button')
        self._destroy_widget('cancel_reg_button1')

    def initializeUI(self):
        self.initializeConsumerName()

    def needsNetwork(self):
        """
        This lets firsboot know that networking is required, in order to
        talk to hosted UEP.
        """
        return True

    def focus(self):
        """
        Focus the initial UI element on the page, in this case the
        login name field.
        """
        # FIXME:  This is currently broken
        login_text = managergui.rhsm_xml.get_widget("account_login")
        login_text.grab_focus()

    def _destroy_widget(self, widget_name):
        """
        Destroy a widget by name.

        See gtk.Widget.destroy()
        """
        widget = managergui.rhsm_xml.get_widget(widget_name)
        widget.destroy()

