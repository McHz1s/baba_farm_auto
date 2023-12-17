from driver.taobao import Taobao
from utils.appium_utils import retry_n


def main():
    seed = {
        'keyword': 'Python 书'
    }
    spider = Taobao()
    while True:
        spider.execute(seed=seed)


if __name__ == '__main__':
    main()
