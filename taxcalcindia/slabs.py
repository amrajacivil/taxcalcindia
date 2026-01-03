from typing import Dict, List, Tuple, Union
from types import MappingProxyType

Number = Union[int, float]
Slab = Tuple[Number, float]

def _base_slabs() -> Dict[str, List[Slab]]:
    """
    Declarative slab definitions. 
    can continue to use 'new_regime', 'old_regime_general', etc.
    """
    return {
        "new_regime": [
            (400000, 0.0),
            (800000, 0.05),
            (1200000, 0.10),
            (1600000, 0.15),
            (2000000, 0.20),
            (2400000, 0.25),
            (float("inf"), 0.30),
        ],
        "old_regime_general": [
            (250000, 0.0),
            (500000, 0.05),
            (1000000, 0.20),
            (float("inf"), 0.30),
        ],
        "old_regime_senior": [
            (300000, 0.0),
            (500000, 0.05),
            (1000000, 0.20),
            (float("inf"), 0.30),
        ],
        "old_regime_super_senior": [
            (500000, 0.0),
            (1000000, 0.20),
            (float("inf"), 0.30),
        ],
    }

def get_tax_slabs(financial_year: Union[int, str] | None, age: int | None) -> Dict[str, List[Slab]]:
    """
    Return tax slabs for the given financial_year and age.
    Currently financial_year is accepted for future extensibility; all years
    use the same base slabs. 
    """
    # Placeholder: adjust slabs based on financial_year if needed in future.
    slabs = _base_slabs()

    immutable = {k: tuple(v) for k, v in slabs.items()}
    return MappingProxyType(immutable)