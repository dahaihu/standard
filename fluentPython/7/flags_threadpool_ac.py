from concurrent import futures
from flags_threadPool import download_one
from flags import POP20_CC


def download_many(cc_list):
    cc_list = cc_list[:5]
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = 'Scheduled for {}: {}'
            print(msg.format(cc, future))
        results = []
        # as_completed 函数在期物运行结束后产出期物
        for future in futures.as_completed(to_do):
            # 会阻塞这个线程，直到执行完成
            # 这种情况下，并不会阻塞线程，因为as_completed会在运行结束后产生期物
            res = future.result()
            msg = '{} result: {!r}'
            print(msg.format(future, res))
            results.append(res)
    return len(results)

if __name__ == '__main__':
    download_many(POP20_CC)
