from artificial_idiot.search.search_cutoff.cutoff import (
    DepthLimitCutoff, Cutoff
)

if __name__ == '__main__':
    cutoff.DepthLimitCutoff
    cutoff = DepthLimitCutoff(max_depth=10)
    assert(cutoff(None, depth=10) == False)
    assert(cutoff(None, depth=9) == False)
    assert(cutoff(None, depth=11) == True)
