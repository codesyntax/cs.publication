try:
    from cs.folderishpage.folderishpage import IFolderishPage as IContextFolder
except:
    from plone.app.contenttypes.interfaces import IFolder as IContextFolder
from Acquisition import aq_inner
from five import grok
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.interfaces import IImageScaleTraversable
from zope import schema
from cs.publication import MessageFactory as _


# Interface class; used to define content-type schema.
class IPublication(form.Schema, IImageScaleTraversable):
    """
    Dexterity publication content
    """
    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/publication.xml to define the content type
    # and add directives here as necessary.
    image = NamedBlobImage(
            title=_(u"Lead Image"),
            description=u"",
            required=False,
        )

    publication_file = NamedBlobFile(title=_(u'File'),
                        required=True,
                        )


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.
class Publication(dexterity.Container):
    grok.implements(IPublication)
    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# templates called publicationview.pt .
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@view" appended unless specified otherwise
# using grok.name below.
# This will make this view the default view for your content-type
grok.templatedir('templates')


class PublicationView(grok.View):
    grok.context(IPublication)
    grok.require('zope2.View')
    grok.name('view')

    def files(self):
        context = aq_inner(self.context)
        return context.getFolderContents({'portal_type': 'File'}, full_objects=1)


class PublicationsView(grok.View):
    grok.context(IContextFolder)
    grok.require('zope2.View')
    grok.name('publications_view')

    def publications(self):
        context = aq_inner(self.context)
        return context.getFolderContents({'portal_type': 'Publication', 'review_state':'published'}, full_objects=1)