from ffxiahbot.auction.worker import Worker
from ffxiahbot.logutils import capture, logger
from ffxiahbot.tables.auctionhouse import AuctionHouse


class Cleaner(Worker):
    """
    Auction House cleaner.

    :param db: database object
    """

    def __init__(self, db, **kwargs):
        super().__init__(db, **kwargs)

    def clear(self, seller=None):
        """
        Clear out auction house.
        """
        # clear rows
        if seller is None:
            # perform query
            with self.scopped_session() as session:
                n = session.query(AuctionHouse).delete()
                logger.info("%d rows dropped", n)

        # clear rows of seller
        else:
            # validate seller
            with capture(fail=self.fail):
                if not isinstance(seller, int) or not seller >= 0:
                    raise RuntimeError("invalid seller: %s", seller)

                # perform query
                with self.scopped_session() as session:
                    n = (
                        session.query(AuctionHouse)
                        .filter(
                            AuctionHouse.seller == seller,
                        )
                        .delete()
                    )
                    logger.info("%d rows dropped", n)
