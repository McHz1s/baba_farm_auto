import argparse
import multiprocessing

from driver.taobao import Taobao
from driver.alipay import Alipay
from utils.appium_utils import retry_n


def parse_args():
    parser = argparse.ArgumentParser(description='config')
    parser.add_argument('--app',
                        nargs='?',
                        type=str,
                        default='Taobao',
                        help='Configuration file to use', )
    return parser.parse_args()

def main():
    args = parse_args()
    seed = {
        'keyword': args.app,
    }
    spider = globals()[args.app]()
    while True:
        spider.execute(seed)


if __name__ == '__main__':
    exit_code = 1
    while exit_code != 0:
        process = multiprocessing.Process(target=main)
        process.start()
        process.join()
        exit_code = process.exitcode
        print(f"Process ended with exit code: {exit_code}")
