import dataclasses
from typing import Annotated, Any, Callable, Concatenate, Self


@dataclasses.dataclass
class User:
    id: int
    username: str


class copy_signature[**P, T]:
    def __init__(self, target: Callable[P, T]):
        pass

    @classmethod
    def from_method[S](cls, target: Callable[Concatenate[S, P], T]) -> Self:
        return cls.__new__(cls)

    def __call__(self, wrapped: Callable[P, T]) -> Callable[P, T]:
        return wrapped

    def to_method[S](self, wrapped: Callable[Concatenate[S, P], T]) -> Callable[Concatenate[S, P], T]:
        return wrapped


@copy_signature(User)
def create_user(*args: Any, **kwargs: Any) -> User:
    return User(*args, **kwargs)


class Repo:
    @copy_signature(User).to_method
    def create_user(self, *args: Any, **kwargs: Any) -> User:
        return User(*args, **kwargs)

    @copy_signature(User)
    @staticmethod
    def static_create_user(*args: Any, **kwargs: Any) -> User:
        return User(*args, **kwargs)

    @copy_signature(User).to_method
    @classmethod
    def cls_create_user(cls, *args: Any, **kwargs: Any) -> User:
        return User(*args, **kwargs)


class Repo2:
    @copy_signature.from_method(Repo.create_user).to_method
    def create_user(self, *args: Any, **kwargs: Any) -> User:
        return Repo().create_user(*args, **kwargs)

    #@copy_signature(Repo.static_create_user)
    @copy_signature.from_method(Repo.create_user)
    @staticmethod
    def static_create_user(*args: Any, **kwargs: Any) -> User:
        return Repo().create_user(*args, **kwargs)

    #@copy_signature(Repo.cls_create_user).to_method
    @copy_signature.from_method(Repo.create_user).to_method
    @classmethod
    def cls_create_user(cls, *args: Any, **kwargs: Any) -> User:
        return Repo().create_user(*args, **kwargs)


from typing import reveal_type
repo = Repo()

reveal_type(create_user)
print(repr(create_user(id=1, username='entwanne')))
#print(repr(create_user(id='1', username='entwanne')))

reveal_type(Repo.create_user)
print(repr(Repo.create_user(Repo(), id=1, username='entwanne')))
#print(repr(Repo.create_user(None, id=1, username='entwanne')))
reveal_type(repo.create_user)
print(repr(repo.create_user(id=1, username='entwanne')))
#print(repr(repo.create_user(id='1', username='entwanne')))

reveal_type(Repo.static_create_user)
print(repr(Repo.static_create_user(id=1, username='entwanne')))
reveal_type(repo.static_create_user)
print(repr(repo.static_create_user(id=1, username='entwanne')))

reveal_type(Repo.cls_create_user)
print(repr(Repo.cls_create_user(id=1, username='entwanne')))
reveal_type(repo.cls_create_user)
print(repr(repo.cls_create_user(id=1, username='entwanne')))

repo2 = Repo2()
reveal_type(Repo2.create_user)
print(repr(Repo2.create_user(Repo2(), id=1, username='entwanne')))
reveal_type(repo2.create_user)
print(repr(repo2.create_user(id=1, username='entwanne')))
#print(repr(repo2.create_user(id='1', username='entwanne')))

reveal_type(Repo2.static_create_user)
print(repr(Repo2.static_create_user(id=1, username='entwanne')))
reveal_type(repo2.static_create_user)
print(repr(repo2.static_create_user(id=1, username='entwanne')))

reveal_type(Repo2.cls_create_user)
print(repr(Repo2.cls_create_user(id=1, username='entwanne')))
reveal_type(repo2.cls_create_user)
print(repr(repo2.cls_create_user(id=1, username='entwanne')))
