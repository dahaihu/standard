"""
给定一个字符串，你需要反转字符串中每个单词的字符顺序，同时仍保留空格和单词的初始顺序。

示例 1:

输入: "Let's take LeetCode contest"
输出: "s'teL ekat edoCteeL tsetnoc"
注意：在字符串中，每个单词由单个空格分隔，并且字符串中不会有任何额外的空格。
"""


class Solution(object):
    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        res = ''
        left = right = 0
        for ele in s:
            if ele == ' ':
                res += s[right - 1:left - 1:-1] + ' '
                left = right = right + 1
            else:
                right += 1
        res += s[right - 1:left - 1:-1]
        return res


string = "enuk$)g*)(mex%y*ocdafa)ev%konbr(ucvu*kjh$kyz*djrk)rniq##jbqtwhu*r&q#gsd#ivkni (xkpffov(frqu)!&sf&stbw)@s! eq&tj)vguf!y$sstm^! @mx%khlj$jpqs*uxwxvgu vjmlw^ubivqyyljta%q&$f@mcvc&(owvgyehq#qph*fak tqxtey kexylyiwh%!bxpcqo@zgg&tklpw%phs)cbo@(&^^wn w*xhpxa@d!!vwavwqchbfmpl&z@$kztz#nc%@!tv$htr!&d(wbj^tcfpu!z)!hyf^&sc!c)z%bgufbj#obhlykh ih$vxc*to#*wombce*eo)pqftfps^c(&kf%clklc f&$murkgdhnos$%ovvaqc&las%r%s*x^cpqvk&xlbmxejlsyt^(ck$ @)ks$i!dotdz)skwc&s^zk!ma!z@ymd%d)(flj^)va*tr^xnjgd!x b!al&bvewa#wtr^pov v$aie%x&&bx#@mnwrvu&^v$je(#se&y)x$wmgzmi!%eixawazf%*g$obyggoybw#ygjg**u(it@^b)@raa#ua(w*wxensgd u(a%qinf#wgoxt(q!&rz)ktpuqrjswqr^kispf*gzv#nkyg icd)xfhdpwwvm@i$%&ov(xkbe)igwajs@v)nepqtbjtk $dexm*bapttglgj$azwcaobdj&$ol#jnoq(f&twe@ulovnliefy%(%uncco%z#%%&w@xanjxdd"
s = Solution()
print(s.reverseWords(string))
