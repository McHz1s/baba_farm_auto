from driver.alipay import Alipay
from utils.appium_utils import retry_n


# @retry_n(5)
def main():
    seed = {
        'keyword': 'Alipay'
    }
    spider = Alipay()
    while True:
        spider.execute(seed=seed)


if __name__ == '__main__':
    main()
