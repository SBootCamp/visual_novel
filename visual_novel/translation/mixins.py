from .models import TranslationItem, TranslationStatisticsChapter

from .errors import (
    TranslationNotFound, InvalidValueOnRowsQuantity
)


class TranslationExistsValidator(object):
    def validate_translation_exists(self, translation_item_id):
        try:
            return TranslationItem.objects.get(
                id=translation_item_id,
            )
        except TranslationItem.DoesNotExist:
            raise TranslationNotFound()


class TranslationChapterExistsValidator(object):
    def validate_chapter_exists(self, chapter_id, translation_item):
        try:
            chapter = TranslationStatisticsChapter.objects.get(
                id=chapter_id,
                tree_id=translation_item.statistics.tree_id
            )
            return
        except TranslationStatisticsChapter.DoesNotExist:
            raise TranslationNotFound()


class InputNumberValidator(object):
    def validate_numbers_input(self, total, translated, edited_first, edited_second, is_chapter):
        # Quantities of rows for chapters are recalculated outside the command
        if is_chapter:
            return

        ttl = int(total)
        trl = int(translated)
        edf = int(edited_first)
        eds = int(edited_second)

        # Validate rows' numbers consistency
        if (trl > ttl) or (edf > trl) or (eds > edf):
            raise InvalidValueOnRowsQuantity()

        return
