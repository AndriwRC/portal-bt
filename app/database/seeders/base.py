from sqlmodel import Session


class BaseSeeder:
    def run(self, db: Session):
        raise NotImplementedError
