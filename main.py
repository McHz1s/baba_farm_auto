from driver.taobao import Taobao
from utils.appium_utils import retry_n


def main():
    seed = {
        'keyword': 'Taobao'
    }
    spider = Taobao()
    while True:
        spider.execute(seed)


if __name__ == '__main__':
    main()
