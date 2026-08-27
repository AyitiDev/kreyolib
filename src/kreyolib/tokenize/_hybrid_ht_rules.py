from yasbd.rules.fr import FrRules
from yasbd.rules.ht import HtRules


class HybridHtRules(HtRules):
    """Extend the base Haitian rules with some French awareness abbreviations."""

    # Add some social / professional abbreviations
    TITLE_ABBRVS = HtRules.TITLE_ABBRVS | {
        "a.c.n",
        "ch.-l",
        "e.v",
        "me",
        "mm",
        "r.p",
    }

    # Remove "est" since it can be a French word and should not be protected
    REFERENCE_ABBRVS = HtRules.REFERENCE_ABBRVS - {"est"}

    SECTION_MARKERS = HtRules.SECTION_MARKERS | FrRules.SECTION_MARKERS
    INLINE_ONLY_ABBRVS = HtRules.INLINE_ONLY_ABBRVS | FrRules.INLINE_ONLY_ABBRVS
    DATE_ABBRVS = HtRules.DATE_ABBRVS | FrRules.DATE_ABBRVS
    COMMON_SENT_STARTERS = HtRules.COMMON_SENT_STARTERS | FrRules.COMMON_SENT_STARTERS


# Entry point for yasbd-lib, so it can detect the rules
PROFILES = [HybridHtRules]
