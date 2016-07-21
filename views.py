from django.shortcuts import render
from .models import Version, Book, Bible, Heading
import re


def get_bible(request, *bible_ref):
    default_version_code = 'CUNP-ST'
    verse = re.findall(r'[0-9:\-]*$', bible_ref[0])[0]
    book_name = re.sub('%s$'%verse, '', bible_ref[0])
    chapter_end = -1
    verse_end = -1
    if re.search(':', verse):
        chapter = re.sub(':[0-9\-]*$', '', verse)
        verse = re.sub('^[0-9\-]*:', '', verse)
    else:
        chapter = verse
        verse = 0
    if re.search('^[0-9]$', chapter):
        chapter = int(chapter)
    elif re.search('^[0-9]*-', chapter):
        if re.search('[0-9]$', chapter):
            chapter_end = int(re.sub('^.*-', '', chapter))
        else:
            chapter_end = 0
        chapter = int(re.sub('-.*$', '', chapter))
    if isinstance(verse, str):
        if re.search('^[0-9]$', verse):
            verse = int(verse)
        elif re.search('[0-9]*-', verse):
            if re.search('[0-9]$', verse):
                verse_end = int(re.sub('^.*-', '', verse))
            else:
                verse_end = 0
            verse = int(re.sub('-.*$', '', verse))
    version = Version.objects.get(code=default_version_code)
    book = Book.objects.filter(version=version, name=book_name)
    if book[0].parent is None:
        book = book[0]
    else:
        book = book[0].parent
    bible_args = {'book': book}
    if verse > 0:
        if verse_end < 0:
            bible_args['verse'] = verse
        else:
            bible_args['verse__gte'] = verse
            if verse_end > 0 and verse_end > verse:
                bible_args['verse__lte'] = verse_end
    if chapter_end >= 0:
        bible_args['chapter__gte'] = chapter
        if chapter_end > 0 and chapter_end > chapter:
            bible_args['chapter__lte'] = chapter_end
    else:
        bible_args['chapter'] = chapter
    bible = Bible.objects.filter(**bible_args)
    bible.ref = bible_ref
    bible.book = book_name
    bible.chapter = chapter
    bible.verse = verse

    return render(request, 'bibleapi/bible.html', {'bible': bible})
