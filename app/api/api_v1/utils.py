

def get_category_data(post):
    if post.category:
        return {
            "id": post.category.id,
            "title": post.category.title,
        }
    return None
