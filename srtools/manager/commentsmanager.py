"""Comments Manager"""
from srtools.manager.basemanager import BaseManager

class CommentsManager(BaseManager):
    """Showroom Comments Manager."""

    class Comment(object):
        """Showroom comment information."""
        def __init__(self, user_id, name, comment,
                     created_at=None, avatar_id=None, avatar_url=None):
            self.user_id = user_id
            self.name = name
            self.comment = comment
            self.created_at = created_at
            self.avatar_id = avatar_id
            self.avatar_url = avatar_url

    class CommentsFilter(object):
        """Showroom comment filter."""
        def __init__(self):
            self.live_id = None
            self.user_id = None
            self.name = None
            self.comment = None

    def __init__(self, configuration, showroom_api):
        super(CommentsManager, self).__init__(configuration, showroom_api)
        self._comments = []

    def create(self, live, user, comment):
        """Creates and returns a new comment with the given information."""
        comment = self.Comment(user.user_id, user.name, comment)
        self._comments[live.live_id].append(comment)
        return comment

    def create_filter(self):
        """Returns a comment filter."""
        return self.CommentsFilter()

    def comments(self, comments_filter=None):
        """Returns a list of comments matching the requirements"""
        if comments_filter is None:
            comments_filter = self.CommentsFilter()

        return [x for x in self._comments[comments_filter.live_id].values() \
                if (comments_filter.user_id is None or (x.user_id == comments_filter.user_id)) and \
                (comments_filter.name is None or (x.name == comments_filter.name)) and \
                (comments_filter.comment is None or (x.comment == comments_filter.comment))]
