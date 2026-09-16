# 成都 · 银杏茶街

一个程序化生成的 Unity 3D 城市街景项目。画面采用风格化几何造型、银杏金黄与青灰建筑配色，表现成都老街与现代城市并置的傍晚氛围。街道是原创组合，不是实际街区或地标的测绘复刻。

## 打开项目

1. 在 Unity Hub 中选择 **Add / 从磁盘添加项目**，选择本文件所在的 `ChengduStreet` 文件夹。
2. 使用 **Unity 2022.3 LTS** 打开，项目按 **2022.3.62f1 / Built-in Render Pipeline** 准备。若 Hub 提示版本未安装，可选择本机已有的 2022.3 LTS 编辑器。其他版本尚未验证。
3. 等待脚本导入完成，双击 `Assets/Scenes/Chengdu.unity`，点击 **Play**，会在运行时生成街景。
4. 如需在编辑器中查看、调整与保存场景，点击菜单 **Chengdu → Generate and save street scene**。生成的物体保存在场景中，材质保存在 `Assets/Generated/Materials`。重新生成会重建整个街景，因此请先另存手动修改的版本。

## 场景内容

- 约 80 米双向街道、自行车道、斑马线、石板人行道。
- 八间双层灰瓦店铺：盖碗茶馆、火锅、担担面、书店、咖啡与小吃。
- 银杏行道树、落叶、灯笼、暖色路灯、室外茶座。
- 熊猫公共雕塑、共享单车、出租车、电动车与行人。
- 远景现代楼群与虚构观景塔。
- 自由镜头、自动环绕展示和 1920×1080 图片导出菜单。

## 操作

| 按键 | 功能 |
| --- | --- |
| WASD | 移动镜头 |
| 按住鼠标右键 | 转动视角 |
| Q / E | 下降 / 上升 |
| 左 Shift | 加速 |
| Tab | 切换自动环绕 |
| R | 恢复初始视角 |
| Esc | 停止环绕 |

运行后先点击 Game 窗口使其获得焦点。镜头为自由摄影模式，没有碰撞限制。使用旧版 Input Manager；若移植到其他工程，请将 Active Input Handling 设为 Input Manager 或 Both。

## 导出图片

先通过菜单生成街景，再选 **Chengdu → Capture game view to PNG**。也可以在 Play 模式中调整镜头后导出；导出图片不包含操作提示。

## 实现与验证范围

场景使用 Unity 内置几何体与 Standard 材质，无 Asset Store 资源依赖。中文招牌已生成为 PNG，因此运行不依赖中文字体。招牌图片通过本机微软雅黑生成；工程不包含字体文件。

当前制作环境没有检测到 Unity 编辑器，所以未完成 Unity 内编译、运行或视觉验收，也没有提供伪称为 Unity 渲染的预览图。已检查脚本语法、资源名称、场景脚本引用和项目文件结构；首次导入后的实际表现需要在 Unity 中验证。

如需命令行生成完整场景，可在安装并激活 Unity 后执行：

```powershell
& '你的Unity编辑器路径\Unity.exe' -batchmode -projectPath '本项目绝对路径' -executeMethod ChengduSceneTools.Generate -quit -logFile 'chengdu-build.log'
```

几何布局与配色见 `Assets/Scripts/ChengduStreet.cs`；镜头见 `Assets/Scripts/StreetCamera.cs`；编辑器生成、保存和截图见 `Assets/Editor/ChengduSceneTools.cs`。
