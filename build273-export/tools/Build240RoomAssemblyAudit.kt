import com.diamondrush.legacy.*
import java.util.zip.ZipFile
import java.io.File

fun main(args: Array<String>) {
    require(args.size == 3) { "usage: <original.jar> <archive-name> <room-index>" }
    val jarPath = args[0]
    val archiveName = args[1]
    val roomIndex = args[2].toInt()
    val bytes = ZipFile(jarPath).use { zip ->
        zip.getInputStream(zip.getEntry(archiveName)).use { it.readBytes() }
    }
    val decoded = LegacyWorldRoomArchiveDecoder.decode(bytes, archiveName, roomIndex)
    val pass = LegacyRoomRenderAssembly.assemble(decoded.room, LegacyCameraOffset(0, 0))
    val output = File("research/build240_${archiveName.removeSuffix(".bin")}_room${roomIndex}_camera0_manifest.csv")
    output.writeText(pass.canonicalCsv())
    val inBounds = pass.cells.filter { it.inBounds }
    println("archive=$archiveName room=$roomIndex dimensions=${decoded.room.planes.firstDimension}x${decoded.room.planes.secondDimension}")
    println("camera=0,0 candidates=${pass.cells.size} inBounds=${pass.inBoundsCount} outOfBounds=${pass.outOfBoundsCount}")
    println("overlayRoutes=${pass.overlayRouteCount} f3=${inBounds.count { it.overlayRoute?.resourceIndex == 3 }} f42_direct=${inBounds.count { it.overlayRoute?.resourceIndex == 42 }}")
    println("output=${output.path}")
}
