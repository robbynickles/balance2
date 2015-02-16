# Not in use, but it defines a sort of abstract class for game objects to implement.

class GameObject():
    '''GameObject facade.
    '''

    @property
    def update( self ):
        return self._update()

    def remove(self):
        self._remove()

    # private

    def _update(self):
        raise NotImplementedError()

    def _remove(self):
        raise NotImplementedError()

