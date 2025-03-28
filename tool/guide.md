### 分析文档：矩形和圆形净化器净化效果的对比

---

#### **实验描述**

房间大小为 **5 m × 8 m × 3 m**（总空间体积为 \( V = 120 \, m^3
\)），实验模拟了两种空气净化器（矩形和圆形）的净化效果，通过对房间污染物浓度分布的模拟，比较了两种净化器在净化后的污染物浓度分布以及净化效果。

净化效果的评估基于以下指标：

1. **污染物浓度的分布热图**：展示净化后不同位置的污染物浓度。
2. **污染物浓度的总方差**：用于衡量净化后污染物浓度的均匀性，方差越小，说明净化效果越好。

---

#### **实验结果**

1. **净化效果热图**
    - **矩形净化器**和**圆形净化器**的热图显示，在净化后，污染物浓度在整个房间趋于均匀，并且边界区域的浓度略高。
    - 两者的热图几乎一致，说明两种净化器在净化污染物时表现相似。

2. **净化效果数值**
    - 矩形净化器的污染物浓度总方差：`0.0684`
    - 圆形净化器的污染物浓度总方差：`0.0684`
    - 两者的污染物浓度总方差完全相同，表明两种净化器在实验条件下净化效果无显著差异。

---

#### **为什么矩形和圆形净化器的净化效果相同？**

1. **初始污染物分布的均匀性**
    - 实验中，污染物初始分布为随机均匀分布。这种情况下，无论净化器的形状如何，其覆盖区域都能够有效地清除污染物，而扩散过程进一步均匀化了污染物的分布，掩盖了两者的形状差异。

2. **房间大小与净化器尺寸的比例**
    - 房间的矩形比例（5 m × 8 m × 3 m）较大，但净化器的覆盖范围（矩形净化器为 \(1 \, \text{m} × 0.5 \, \text{m} × 1.5 \,
      \text{m}\)，圆形净化器半径为 1.0 m）相对于房间而言较小，无法显著影响整体空气流动。因此，净化效果的区域性差异不够明显。

3. **扩散模型的影响**
    - 模拟过程中采用了扩散系数 (\( \alpha = 0.1 \)) 的扩散公式，模拟污染物浓度在房间内的自然扩散。这种扩散作用在整个房间均匀发生，进一步减弱了两种净化器在边界区域的净化效果差异。

4. **净化器位置**
    - 两种净化器均放置在房间的中心位置，使得它们的净化范围在空间上均匀分布，这种对称性进一步减少了两种净化器在净化效果上的差异。

---

#### **后期优化的思路**

1. **调整污染物初始分布**
    - 当前实验中的污染物初始分布为随机均匀分布，缺乏实际情境下可能出现的污染源集中现象。可以模拟以下场景：
        - **局部污染源**：如某一角落污染物浓度较高。
        - **线性污染源**：如沿房间长边或宽边分布的污染物。
    - 通过改变初始分布，观察两种净化器在不同污染分布下的效果差异。

2. **优化净化器尺寸和位置**
    - 当前净化器的尺寸较小，相对于房间体积而言覆盖面积有限。可以优化净化器的尺寸，使其覆盖更大范围。
    - 研究净化器的最佳放置位置，例如靠近污染源或靠近房间角落。

3. **考虑空气流动的方向性**
    - 模拟空气净化器的风向（进风口和出风口的设置），以及不同形状净化器对空气流动路径的影响。这种设置可以更真实地模拟实际空气流动路径。

4. **增加净化时间的评估**
    - 当前实验只进行了固定迭代步数（100 步）的模拟，可以将时间引入为一个变量，评估净化器达到目标浓度所需的时间，进一步衡量两种净化器的净化效率。

5. **房间边界条件**
    - 考虑房间的墙壁、天花板、地板等边界对空气流动和净化效果的影响。当前模型假设边界是完全封闭的，可以尝试引入空气外泄或补充的边界条件。

6. **调整净化器形状和性能参数**
    - 矩形净化器可以增加多面进风口设计，以覆盖更大范围。
    - 圆形净化器可以通过增加半径或提高风量，来改善其在边界区域的净化效果。

---

#### **总结**

通过本次实验和分析，我们可以得出以下结论：

1. 在当前实验条件下（均匀污染分布、固定净化器位置和尺寸），矩形和圆形净化器的净化效果相同，难以看出形状对净化效果的影响。
2. 这种现象主要受到污染物扩散模型和初始条件的影响。
3. 后期优化可以通过调整污染分布、优化净化器设计、引入空气流动路径等方式来进一步分析两种形状净化器的效果差异。

这些优化方法将帮助我们更深入地理解不同形状净化器在复杂场景下的实际表现。