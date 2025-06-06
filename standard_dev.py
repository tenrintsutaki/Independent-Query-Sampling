from itertools import permutations

if __name__ == '__main__':
    class ListNode(object):
        def __init__(self, val=0, next=None):
            self.val = val
            self.next = next
    def reverseKGroup(head, k):
        """
        :type head: Optional[ListNode]
        :type k: int
        :rtype: Optional[ListNode]
        """
        dummy = head  # 1,2,3,4,5
        copied = []
        while dummy:
            copied.append(dummy)
            dummy = dummy.next
        for i in range(0, len(copied), k):
            if k == len(copied):
                copied[i:i + k] = reversed(copied[i:i + k])
                break
            if i + k < len(copied):
                copied[i:i + k] = reversed(copied[i:i + k])
        for i in range(0, len(copied) - 1):
            copied[i].next = copied[i + 1]
        head = copied[0]
        copied[-1].next = None
        return copied[0]

n1 = ListNode(1)
n1.next = ListNode(2)

res = reverseKGroup(n1, 2)
while res:
    print(res.val)
    res = res.next