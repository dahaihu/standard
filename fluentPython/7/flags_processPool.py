from concurrent import futures

from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20

"""
开启多个进程，速度却比多个线程更慢
"""


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    # 创建一个线程池
    with futures.ProcessPoolExecutor(workers) as executor:
        # 这个线程池使用map方法
        # 但是返回的结果是什么呢?
        # 这个res是个迭代器，其中每个存储的结果是download_one返回的结果
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))


if __name__ == '__main__':
    main(download_many)