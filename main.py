import heapq
import sys


# ノードコスト計算
def culcNodeCost(graph: dict,
                 queue: list,
                 node: str,
                 min_dst_dict: dict,
                 prev_node_dict: dict):
    for key in graph[node].keys():
        tmp = min_dst_dict[node] + graph[node][key]
        if key not in min_dst_dict.keys() or tmp < min_dst_dict[key]:
            min_dst_dict[key] = tmp
            heapq.heappush(queue, (min_dst_dict[key], key))


# ダイクストラ法
def dijkstra(graph: dict) -> (dict, dict):
    args = sys.argv
    min_dst_dict = {}
    prev_node_dict = {}
    queue = []
    heapq.heappush(queue, (0, args[1]))

    prev_node = ""
    while True:
        dst, node = heapq.heappop(queue)
        min_dst_dict[node] = dst
        prev_node_dict[node] = prev_node

        if node == args[2]:
            return min_dst_dict, prev_node_dict
        else:
            prev_node = node
            culcNodeCost(graph, queue, node, min_dst_dict, prev_node_dict)


# グラフ初期化
def init_graph(data: list) -> dict:
    graph = {}
    for datum in data:
        src = datum[0]
        dst = datum[1]
        cost = int(datum[2])
        graph = init_node(graph, src, dst)
        graph[src][dst] = cost
        graph[dst][src] = cost
    return graph


# 初期ノード追加
def init_node(graph: dict, src: str, dst: str) -> dict:
    if src not in graph.keys():
        graph[src] = {}
    if dst not in graph.keys():
        graph[dst] = {}
    return graph


def culcCostFromTime(before: str, after: str) -> int:
    before = [int(i) for i in before.split(':')]
    after = [int(i) for i in after.split(':')]
    cost = (after[0]*60+after[1]) - (before[0]*60+before[1])
    return cost


# 読み込み
def read_data() -> list:
    args = sys.argv
    times = []
    data = {}
    for i, line in enumerate(sys.stdin):
        if i % 4 == 0:
            names = line.split()
        elif i % 4 >= 1 and i % 4 <= 3:
            times.append(line.split())
        if i % 4 == 3:
            for j, name in enumerate(names):
                if name not in data:
                    data[name] = {}
                for time in times:
                    if time[j] not in data[name]:
                        data[name][time[j]] = []
                    if j < len(names)-1:
                        data[name][time[j]].append({
                            "dst": names[j+1], "dst_time": time[j+1]
                        })
                    else:
                        data[name][time[j]] = []
            times = []
            names = []

    # output: [[src, dst, cost]*n]
    output = []
    for name in data.keys():
        i = 0
        times = sorted(data[name].keys())

        while i < len(times):
            # start, goal 0cost node
            if args[1] == name:
                src = name
                dst = name+times[i]
                output.append([src, dst, 0])
            elif args[2] == name:
                src = name+times[i]
                dst = name
                output.append([src, dst, 0])

            # 乗り換えノード追加
            if i < len(times)-1:
                src = name+times[i]
                dst = name+times[i+1]
                cost = culcCostFromTime(times[i], times[i+1])
                output.append([src, dst, cost])

            # 同線Node to Node追加
            for dst_dict in data[name][times[i]]:
                src = name+times[i]
                dst = dst_dict['dst']+dst_dict['dst_time']
                cost = culcCostFromTime(times[i], dst_dict['dst_time'])
                output.append([src, dst, cost])

            i += 1

    return output


def main():
    data = read_data()
    graph = init_graph(data)
    start_goal, shortest_path = dijkstra(graph)
    print('Min Cost : ' + str(start_goal[sys.argv[2]]))
    print(start_goal)
    print(shortest_path)


if __name__ == "__main__":
    main()
    sys.exit(0)
